CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(255) PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_status ENUM('open', 'in progress', 'completed') NOT NULL,
    tutors TEXT NOT NULL,
    ects INT NOT NULL,
    grade FLOAT
);
