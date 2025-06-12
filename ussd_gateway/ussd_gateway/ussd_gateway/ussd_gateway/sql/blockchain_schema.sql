-- Layer 1: Emergency Access Records
CREATE TABLE emergency_records (
    patient_id VARCHAR(20) PRIMARY KEY,
    blood_type VARCHAR(5),
    allergies TEXT[],
    medications TEXT[],
    last_updated DATE
);

-- Layer 2: Full Medical History (Protected Layer)
CREATE TABLE medical_history (
    record_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20),
    condition TEXT,
    diagnosis_date DATE,
    lab_results TEXT,
    treatment TEXT,
    doctor_id VARCHAR(20),
    access_granted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (patient_id) REFERENCES emergency_records(patient_id)
);

-- Optional: Audit log
CREATE TABLE access_logs (
    log_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20),
    accessed_by VARCHAR(20),
    access_time TIMESTAMP DEFAULT NOW(),
    access_type VARCHAR(10) -- "layer1" or "layer2"
);
