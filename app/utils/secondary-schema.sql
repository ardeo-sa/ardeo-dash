-- Create the metric_catalog table for allowed metric names and descriptions
CREATE TABLE metrics.metric_catalog (
    metric_name VARCHAR(100) PRIMARY KEY,
    description TEXT,
    default_unit VARCHAR(20)
);

-- Insert valid metrics into metric_catalog (same as before)
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


-- Create the tables for storing metrics: operational, mdt, pathway, clinician, referral
CREATE TABLE metrics.operational_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_metric_name FOREIGN KEY (metric_name) REFERENCES metrics.metric_catalog (metric_name)
);

CREATE INDEX idx_operational_metrics_date_name ON metrics.operational_metrics (date, metric_name);


CREATE TABLE metrics.mdt_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_metric_name FOREIGN KEY (metric_name) REFERENCES metrics.metric_catalog (metric_name)
);

CREATE INDEX idx_mdt_metrics_date_name ON metrics.mdt_metrics (date, metric_name);


CREATE TABLE metrics.pathway_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_metric_name FOREIGN KEY (metric_name) REFERENCES metrics.metric_catalog (metric_name)
);

CREATE INDEX idx_pathway_metrics_date_name ON metrics.pathway_metrics (date, metric_name);


CREATE TABLE metrics.clinician_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    clinician_id INTEGER NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_clinician_id FOREIGN KEY (clinician_id) REFERENCES metrics.clinician(id),
    CONSTRAINT fk_metric_name FOREIGN KEY (metric_name) REFERENCES metrics.metric_catalog (metric_name)
);

CREATE INDEX idx_clinician_metrics_date_name ON metrics.clinician_metrics (date, clinician_id, metric_name);


CREATE TABLE metrics.referral_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    referral_id INTEGER NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_referral_id FOREIGN KEY (referral_id) REFERENCES metrics.referral(id),
    CONSTRAINT fk_metric_name FOREIGN KEY (metric_name) REFERENCES metrics.metric_catalog (metric_name)
);

CREATE INDEX idx_referral_metrics_date_name ON metrics.referral_metrics (date, referral_id, metric_name);
