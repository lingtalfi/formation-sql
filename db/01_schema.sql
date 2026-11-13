-- =====================================================================
--  Base d'entraînement : essais_cliniques
--  Formation « Langage SQL » — données 100 % fictives
--  Cible : MySQL 8
--
--  Date de référence des données (« aujourd'hui » dans la base) : 2026-06-30
--  → toutes les dates postérieures sont des dates prévues, pas encore réalisées.
-- =====================================================================

-- Le fichier est encodé en UTF-8 : on l'indique au serveur avant tout
-- (sinon les accents peuvent être mal enregistrés selon le client utilisé).
SET NAMES utf8mb4;

DROP DATABASE IF EXISTS essais_cliniques;
CREATE DATABASE essais_cliniques
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
USE essais_cliniques;

-- ---------------------------------------------------------------------
--  etude : un essai clinique (un protocole)
-- ---------------------------------------------------------------------
CREATE TABLE etude (
  id                  INT          NOT NULL AUTO_INCREMENT,
  code                VARCHAR(20)  NOT NULL,
  titre               VARCHAR(200) NOT NULL,
  phase               VARCHAR(3)   NOT NULL,
  aire_therapeutique  VARCHAR(50)  NOT NULL,
  promoteur           VARCHAR(100) NOT NULL,
  date_debut          DATE         NULL,          -- NULL = étude pas encore démarrée
  date_fin_prevue     DATE         NULL,
  objectif_inclusions INT          NOT NULL,
  statut              VARCHAR(20)  NOT NULL DEFAULT 'en préparation',
  CONSTRAINT pk_etude          PRIMARY KEY (id),
  CONSTRAINT uq_etude_code     UNIQUE (code),
  CONSTRAINT ck_etude_phase    CHECK (phase IN ('I', 'II', 'III', 'IV')),
  CONSTRAINT ck_etude_objectif CHECK (objectif_inclusions > 0),
  CONSTRAINT ck_etude_statut   CHECK (statut IN ('en préparation', 'recrutement', 'suivi', 'terminée'))
);

-- ---------------------------------------------------------------------
--  centre : un hôpital / une clinique qui participe aux études
-- ---------------------------------------------------------------------
CREATE TABLE centre (
  id    INT          NOT NULL AUTO_INCREMENT,
  nom   VARCHAR(100) NOT NULL,
  ville VARCHAR(50)  NOT NULL,
  pays  VARCHAR(50)  NOT NULL DEFAULT 'France',
  CONSTRAINT pk_centre PRIMARY KEY (id)
);

-- ---------------------------------------------------------------------
--  investigateur : médecin travaillant dans un centre
--  superviseur_id → un autre investigateur (auto-référence)
-- ---------------------------------------------------------------------
CREATE TABLE investigateur (
  id             INT          NOT NULL AUTO_INCREMENT,
  nom            VARCHAR(50)  NOT NULL,
  prenom         VARCHAR(50)  NOT NULL,
  specialite     VARCHAR(50)  NOT NULL,
  email          VARCHAR(100) NOT NULL,
  centre_id      INT          NOT NULL,
  superviseur_id INT          NULL,               -- NULL = chef de service
  CONSTRAINT pk_investigateur             PRIMARY KEY (id),
  CONSTRAINT uq_investigateur_email       UNIQUE (email),
  CONSTRAINT fk_investigateur_centre      FOREIGN KEY (centre_id)      REFERENCES centre (id),
  CONSTRAINT fk_investigateur_superviseur FOREIGN KEY (superviseur_id) REFERENCES investigateur (id)
);

-- ---------------------------------------------------------------------
--  etude_centre : association N–N entre etude et centre
--  (quels centres participent à quelle étude)
-- ---------------------------------------------------------------------
CREATE TABLE etude_centre (
  etude_id                   INT  NOT NULL,
  centre_id                  INT  NOT NULL,
  investigateur_principal_id INT  NOT NULL,
  date_ouverture             DATE NULL,           -- NULL = centre pas encore ouvert
  objectif_inclusions        INT  NOT NULL,
  CONSTRAINT pk_etude_centre               PRIMARY KEY (etude_id, centre_id),
  CONSTRAINT fk_etude_centre_etude         FOREIGN KEY (etude_id)  REFERENCES etude (id),
  CONSTRAINT fk_etude_centre_centre        FOREIGN KEY (centre_id) REFERENCES centre (id),
  CONSTRAINT fk_etude_centre_investigateur FOREIGN KEY (investigateur_principal_id) REFERENCES investigateur (id),
  CONSTRAINT ck_etude_centre_objectif      CHECK (objectif_inclusions > 0)
);

-- ---------------------------------------------------------------------
--  patient : une personne qui a été « screenée » pour une étude
--  date_inclusion NULL = échec de screening (non incluse)
-- ---------------------------------------------------------------------
CREATE TABLE patient (
  id              INT         NOT NULL AUTO_INCREMENT,
  code_patient    VARCHAR(20) NOT NULL,
  etude_id        INT         NOT NULL,
  centre_id       INT         NOT NULL,
  sexe            CHAR(1)     NOT NULL,
  annee_naissance SMALLINT    NOT NULL,
  date_screening  DATE        NOT NULL,
  date_inclusion  DATE        NULL,               -- NULL = échec de screening
  bras            VARCHAR(20) NULL,               -- 'traitement' ou 'placebo' (NULL si non inclus)
  date_sortie     DATE        NULL,               -- NULL = toujours dans l'étude
  motif_sortie    VARCHAR(50) NULL,
  CONSTRAINT pk_patient              PRIMARY KEY (id),
  CONSTRAINT uq_patient_code         UNIQUE (code_patient),
  CONSTRAINT fk_patient_etude        FOREIGN KEY (etude_id)  REFERENCES etude (id),
  CONSTRAINT fk_patient_centre       FOREIGN KEY (centre_id) REFERENCES centre (id),
  -- le centre du patient doit participer à son étude :
  CONSTRAINT fk_patient_etude_centre FOREIGN KEY (etude_id, centre_id) REFERENCES etude_centre (etude_id, centre_id),
  CONSTRAINT ck_patient_sexe         CHECK (sexe IN ('F', 'M')),
  CONSTRAINT ck_patient_bras         CHECK (bras IN ('traitement', 'placebo'))
);

-- ---------------------------------------------------------------------
--  visite : rendez-vous prévus par le protocole pour un patient inclus
--  date_realisee NULL = visite pas (encore) faite
-- ---------------------------------------------------------------------
CREATE TABLE visite (
  id            INT         NOT NULL AUTO_INCREMENT,
  patient_id    INT         NOT NULL,
  type_visite   VARCHAR(5)  NOT NULL,             -- V0 (inclusion) … V6 (fin d'étude)
  date_prevue   DATE        NOT NULL,
  date_realisee DATE        NULL,
  CONSTRAINT pk_visite         PRIMARY KEY (id),
  CONSTRAINT uq_visite         UNIQUE (patient_id, type_visite),
  CONSTRAINT fk_visite_patient FOREIGN KEY (patient_id) REFERENCES patient (id)
);

-- ---------------------------------------------------------------------
--  evenement_indesirable (EI) : problème de santé survenu pendant l'étude
-- ---------------------------------------------------------------------
CREATE TABLE evenement_indesirable (
  id              INT          NOT NULL AUTO_INCREMENT,
  patient_id      INT          NOT NULL,
  date_survenue   DATE         NOT NULL,
  terme           VARCHAR(100) NOT NULL,
  grade           TINYINT      NOT NULL,          -- 1 (léger) … 5 (fatal)
  grave           BOOLEAN      NOT NULL DEFAULT FALSE,
  lien_traitement VARCHAR(20)  NOT NULL,
  date_resolution DATE         NULL,              -- NULL = toujours en cours
  CONSTRAINT pk_evenement_indesirable PRIMARY KEY (id),
  CONSTRAINT fk_ei_patient            FOREIGN KEY (patient_id) REFERENCES patient (id),
  CONSTRAINT ck_ei_grade              CHECK (grade BETWEEN 1 AND 5),
  CONSTRAINT ck_ei_lien               CHECK (lien_traitement IN ('certain', 'probable', 'possible', 'improbable', 'exclu'))
);

-- ---------------------------------------------------------------------
--  mesure : valeurs relevées lors d'une visite réalisée
-- ---------------------------------------------------------------------
CREATE TABLE mesure (
  id        INT          NOT NULL AUTO_INCREMENT,
  visite_id INT          NOT NULL,
  parametre VARCHAR(30)  NOT NULL,                -- poids, pas, pad, glycemie
  valeur    DECIMAL(7,2) NOT NULL,
  unite     VARCHAR(10)  NOT NULL,
  CONSTRAINT pk_mesure        PRIMARY KEY (id),
  CONSTRAINT uq_mesure        UNIQUE (visite_id, parametre),
  CONSTRAINT fk_mesure_visite FOREIGN KEY (visite_id) REFERENCES visite (id)
);
