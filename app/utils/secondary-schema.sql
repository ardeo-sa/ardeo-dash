-- Create schema for metrics
CREATE SCHEMA IF NOT EXISTS metrics;


CREATE TABLE metrics.patient_metrics (
    id SERIAL PRIMARY KEY,
    patient_id UUID NOT NULL,
    date DATE NOT NULL,
    avg_length_of_stay DOUBLE PRECISION,
    admission_count INTEGER,
    discharge_count INTEGER,
    readmission BOOLEAN,
    FOREIGN KEY (patient_id) REFERENCES public.patient(id) ON DELETE CASCADE
);

-- Table to hold individual metric records
CREATE TABLE metrics.operational_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Dimension table for allowed metric names and units
CREATE TABLE metrics.metric_catalog (
    metric_name VARCHAR(100) PRIMARY KEY,
    description TEXT,
    default_unit VARCHAR(20)
);

INSERT INTO metrics.metric_catalog (metric_name, description, default_unit) VALUES
    ('daily_admissions', 'Number of admissions on a given day', 'count'),
    ('daily_discharges', 'Number of discharges on a given day', 'count'),
    ('average_length_of_stay', 'Average inpatient length of stay', 'days'),
    ('average_mdt_wait_time', 'Time between referral and MDT review', 'days'),
    ('readmission_rate_30d', 'Patients readmitted within 30 days', 'count'),
    ('appointment_no_show_rate', 'Rate of missed or cancelled appointments', 'percent'),
    ('bed_occupancy_rate', 'Percentage of beds occupied', 'percent'),
    ('admission_to_treatment_start', 'Days between admission and treatment start', 'days'),
    ('mdt_meeting_count', 'Number of MDT meetings held', 'count'),
    ('mdt_avg_attendance', 'Average number of attendees per MDT meeting', 'people'),
    ('mdt_avg_wait_time', 'Average wait from referral to MDT review', 'days'),
    ('mdt_action_completion_rate', 'Percentage of completed MDT actions', 'percent'),
    ('pathway_adherence_rate', 'Average patient adherence to pathways', 'percent'),
    ('pathway_dropout_rate', 'Percentage of patients dropping out of pathways', 'percent'),
    ('pathway_success_rate', 'Percentage of successful pathway completions', 'percent'),
    ('pathway_failure_rate', 'Percentage of pathway failures', 'percent');

-- Index for fast lookup by date and name
CREATE INDEX idx_operational_metrics_date_name ON metrics.operational_metrics (date, metric_name);


Kroki:

3. update sql script based on updated models