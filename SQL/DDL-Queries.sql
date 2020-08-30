
/* Schema commands to create the drugbank_db database
 * This table layout was chosen to implement a 1st
 * normal form of the data scraped from drugbank.ca
 
 * There is room to improve to a 2nd normal form, in which
 * we may have a master action list, and a master alternate
 * identifier lists. We could then use many-to-many tables
 * to bind them to drugs and targets. This would help reduce
 * the overall number of records, but at the same time would
 * involve even more joining to reproduce the original dataset
 */

CREATE TABLE "drug" (
    "drug_id" VARCHAR   NOT NULL,
    "smiles" VARCHAR   NOT NULL,
    CONSTRAINT "pk_drug" PRIMARY KEY (
        "drug_id"
     )
);

CREATE TABLE "target" (
    "target_id" INT   NOT NULL,
    "drug_id" VARCHAR   NOT NULL,
    "gene_name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_target" PRIMARY KEY (
        "target_id"
     )
);

CREATE TABLE "action" (
    "action_id" INT   NOT NULL,
    "target_id" INT   NOT NULL,
    "action" VARCHAR   NOT NULL,
    CONSTRAINT "pk_action" PRIMARY KEY (
        "action_id"
     )
);

CREATE TABLE "alt_identifier" (
    "alt_identifier_id" INT   NOT NULL,
    "drug_id" VARCHAR   NOT NULL,
    "location" VARCHAR   NOT NULL,
    "name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_alt_identifier" PRIMARY KEY (
        "alt_identifier_id"
     )
);

ALTER TABLE "target" ADD CONSTRAINT "fk_target_drug_id" FOREIGN KEY("drug_id")
REFERENCES "drug" ("drug_id");

ALTER TABLE "action" ADD CONSTRAINT "fk_action_target_id" FOREIGN KEY("target_id")
REFERENCES "target" ("target_id");

ALTER TABLE "alt_identifier" ADD CONSTRAINT "fk_alt_identifier_drug_id" FOREIGN KEY("drug_id")
REFERENCES "drug" ("drug_id");

