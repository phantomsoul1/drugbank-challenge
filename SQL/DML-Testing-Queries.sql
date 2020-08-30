SELECT * FROM action;

SELECT * FROM alt_identifier;

SELECT * FROM drug;

SELECT * FROM target;

SELECT * 
FROM drug d
LEFT JOIN target t ON d.drug_id = t.drug_id
LEFT JOIN action a ON t.target_id = a.target_id
WHERE d.drug_id = 'DB00619';

SELECT * 
FROM drug d
LEFT JOIN alt_identifier i on d.drug_id = i.drug_id
WHERE d.drug_id = 'DB00619';