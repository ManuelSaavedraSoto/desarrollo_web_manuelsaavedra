-- Cleanup existing test data
DELETE FROM actividad_tema WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM contactar_por WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM foto WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM actividad WHERE email LIKE '%test%';

-- Insert test activities with proper date format and validations
INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion) VALUES
(130208, 'Barrio Universitario', 'Juan Pérez', 'test1@example.com', '+569.12345678', '2025-05-15 14:00:00', '2025-05-15 17:00:00', 'Encuentro musical con bandas universitarias locales'),
(130208, 'Plaza Italia', 'María González', 'test2@example.com', '+569.87654321', '2025-05-20 10:00:00', '2025-05-20 18:00:00', 'Feria tecnológica y exhibición de startups'),
(130210, 'Parque Bustamante', 'Carlos Rodríguez', 'test3@example.com', '+569.23456789', '2025-05-25 09:00:00', '2025-05-25 13:00:00', 'Torneo de fútbol amateur'),
(130214, 'Centro Cultural', 'Ana Silva', 'test4@example.com', '+569.11223344', '2025-06-01 19:00:00', '2025-06-01 22:00:00', 'Exposición de arte contemporáneo'),
(130207, 'Teatro Municipal', 'Roberto Lagos', 'test5@example.com', '+569.99887766', '2025-06-05 20:00:00', '2025-06-05 23:30:00', 'Festival de danza moderna');

-- Add themes for activities with proper enum values
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES
('música', NULL, (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('tecnología', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('ciencias', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('deporte', NULL, (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('otro', 'Arte Urbano', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('baile', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('música', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com'));

-- Add contact methods with proper enum values
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES
('whatsapp', '+569.12345678', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('instagram', '@bandas_univ', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('telegram', '@tech_expo', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('X', '@deportes_stgo', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('instagram', '@arte_contemp', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('tiktok', '@danza_moderna', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('whatsapp', '+569.99887766', (SELECT id FROM actividad WHERE email = 'test5@example.com'));

-- Add sample photos using existing cat pictures
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES
('uploads/cat_1.jpg', 'cat_1.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_2.jpg', 'cat_2.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_3.jpg', 'cat_3.jpg', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('uploads/cat_4.jpg', 'cat_4.jpg', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('uploads/cat_5.jpg', 'cat_5.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_6.jpg', 'cat_6.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_7.jpg', 'cat_7.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_8.jpg', 'cat_8.jpg', (SELECT id FROM actividad WHERE email = 'test5@example.com'));