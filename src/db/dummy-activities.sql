-- Cleanup existing test data
DELETE FROM actividad_tema WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM contactar_por WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM foto WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM actividad WHERE email LIKE '%test%';

-- Insert test activities
INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion) VALUES
(130208, 'Barrio Universitario', 'Juan Pérez', 'test1@example.com', '+569.12345678', '2025-05-15 14:00:00', '2025-05-15 17:00:00', 'Encuentro musical con bandas universitarias locales'),
(130208, 'Plaza Italia', 'María González', 'test2@example.com', '+569.87654321', '2025-05-20 10:00:00', '2025-05-20 18:00:00', 'Feria tecnológica y exhibición de startups'),
(130210, 'Parque', 'Carlos Rodríguez', 'test3@example.com', NULL, '2025-05-25 09:00:00', NULL, 'Torneo de fútbol amateur'),
(130214, 'Centro Cultural', 'Ana Silva', 'test4@example.com', '+569.11223344', '2025-06-01 19:00:00', '2025-06-01 22:00:00', 'Exposición de arte contemporáneo'),
(130207, 'Teatro Municipal', 'Roberto Lagos', 'test5@example.com', '+569.99887766', '2025-06-05 20:00:00', '2025-06-05 23:30:00', 'Festival de danza moderna');

-- Add themes for activities
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES
('música', NULL, (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('tecnología', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('ciencias', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('deporte', NULL, (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('otro', 'Arte Urbano', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('baile', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('música', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com'));

-- Add contact methods
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES
('whatsapp', '+56912345678', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('instagram', '@bandas_universitarias', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('telegram', '@tech_expo', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('X', '@deportes_stgo', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('instagram', '@arte_contemporaneo', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('tiktok', '@danza_moderna', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('whatsapp', '+56999887766', (SELECT id FROM actividad WHERE email = 'test5@example.com'));

-- Add sample photos with new naming convention
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES
('uploads/cat_1.jpg', '1_1.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_2.jpg', '1_2.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_3.jpg', '2_1.jpg', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('uploads/cat_4.jpg', '3_1.jpg', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('uploads/cat_5.jpg', '4_1.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_6.jpg', '4_2.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_7.jpg', '4_3.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_8.jpg', '5_1.jpg', (SELECT id FROM actividad WHERE email = 'test5@example.com'));