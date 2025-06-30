-- Cleanup existing test data
DELETE FROM comentario WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM actividad_tema WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM contactar_por WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM foto WHERE actividad_id IN (SELECT id FROM actividad WHERE email LIKE '%test%');
DELETE FROM actividad WHERE email LIKE '%test%';

-- Insert test activities with proper date format and validations
INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion) VALUES
(130208, 'Barrio Universitario', 'Laura Martínez', 'test1@example.com', '+569.12345678', '2025-05-15 14:00:00', NULL, 'Festival Gatuno Musical: Un encuentro musical único donde nuestros felinos amigos serán los protagonistas. Música en vivo, adopción de gatos y mucha diversión.'),
(130208, 'Plaza Italia', 'Pedro Soto', 'test2@example.com', '+569.87654321', '2025-05-20 10:00:00', '2025-05-20 18:00:00', 'TechCat Expo 2025: La primera feria tecnológica dedicada a innovaciones para mascotas. Robots alimentadores, juguetes inteligentes y más.'),
(130210, 'Parque Bustamante', 'Ana Rojas', 'test3@example.com', '+569.23456789', '2025-05-25 09:00:00', NULL, 'Gatos en Movimiento: Exhibición deportiva y juegos para gatos. Competencias de agilidad, carreras de obstáculos y premios para los más ágiles.'),
(130214, 'Centro Cultural', 'Carlos Muñoz', 'test4@example.com', '+569.11223344', '2025-06-01 19:00:00', '2025-06-01 22:00:00', 'Galería Felina: Una exposición única de fotografía y arte inspirada en nuestros amigos felinos. Obras de artistas locales y internacionales.'),
(130207, 'Teatro Municipal', 'Isabel Flores', 'test5@example.com', '+569.99887766', '2025-06-05 20:00:00', NULL, 'Gatitos Bailarines: Un espectáculo de danza contemporánea inspirado en el movimiento natural de los gatos. Música, luces y gracilidad felina.'),
(130206, 'Parque Forestal', 'Diego Vargas', 'test6@example.com', '+569.55443322', '2025-06-10 15:00:00', '2025-06-10 19:00:00', 'Ciencia Gatuna: Charlas científicas sobre comportamiento felino, evolución y curiosidades de los gatos. Con demostraciones en vivo.'),
(130205, 'Plaza de Armas', 'Valentina Parra', 'test7@example.com', '+569.77889900', '2025-06-15 11:00:00', NULL, 'GatoCon 2025: La convención más grande de amantes de los gatos. Stands, charlas, concursos y área de adopción.'),
(130209, 'Parque OHiggins', 'Manuel Castro', 'test8@example.com', '+569.44556677', '2025-06-20 16:00:00', '2025-06-20 19:00:00', 'Gatos y Política: Debate sobre políticas de protección animal y derechos de las mascotas. Con la participación de autoridades locales.');

-- Add themes for activities with proper enum values
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES
('música', NULL, (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('otro', 'Adopción', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('tecnología', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('ciencias', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('juegos', NULL, (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('deporte', NULL, (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('juegos', NULL, (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('otro', 'Arte Felino', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('música', NULL, (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('baile', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('música', NULL, (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('ciencias', NULL, (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('tecnología', NULL, (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('otro', 'Educación', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('otro', 'Mascotas', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('tecnología', NULL, (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('política', NULL, (SELECT id FROM actividad WHERE email = 'test8@example.com')),
('otro', 'Derechos', (SELECT id FROM actividad WHERE email = 'test8@example.com'));

-- Add contact methods with proper enum values
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES
('whatsapp', '+569.12345678', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('instagram', '@festival_gatuno', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('telegram', '@techcat_expo', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('instagram', '@techcat2025', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('whatsapp', '+569.23456789', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('x', '@gatos_deportivos', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('instagram', '@galeria_felina', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('telegram', '@arte_gatos', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('tiktok', '@danza_gatitos', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('instagram', '@danza_felina', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('whatsapp', '+569.55443322', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('x', '@ciencia_gatos', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('instagram', '@gaticon2025', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('telegram', '@gaticon_cl', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('whatsapp', '+569.44556677', (SELECT id FROM actividad WHERE email = 'test8@example.com')),
('x', '@gatos_pol', (SELECT id FROM actividad WHERE email = 'test8@example.com'));

-- Add sample photos using existing cat pictures
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES
('uploads/cat_1.jpg', 'cat_1.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_2.jpg', 'cat_2.jpg', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('uploads/cat_3.jpg', 'cat_3.jpg', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('uploads/cat_4.jpg', 'cat_4.jpg', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('uploads/cat_5.jpg', 'cat_5.jpg', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('uploads/cat_6.jpg', 'cat_6.jpg', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('uploads/cat_7.jpg', 'cat_7.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_8.jpg', 'cat_8.jpg', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('uploads/cat_1.jpg', 'cat_1.jpg', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('uploads/cat_2.jpg', 'cat_2.jpg', (SELECT id FROM actividad WHERE email = 'test5@example.com')),
('uploads/cat_3.jpg', 'cat_3.jpg', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('uploads/cat_4.jpg', 'cat_4.jpg', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('uploads/cat_5.jpg', 'cat_5.jpg', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('uploads/cat_6.jpg', 'cat_6.jpg', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('uploads/cat_7.jpg', 'cat_7.jpg', (SELECT id FROM actividad WHERE email = 'test8@example.com')),
('uploads/cat_8.jpg', 'cat_8.jpg', (SELECT id FROM actividad WHERE email = 'test8@example.com'));

-- Comments for activities
INSERT INTO comentario (nombre, texto, fecha, actividad_id) VALUES
('Juan Pérez', 'Me encantan los festivales gatunos, ¡definitivamente asistiré!', '2025-05-10 15:30:00', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('María Silva', '¿Habrá zona de adopción para gatitos rescatados?', '2025-05-12 18:45:00', (SELECT id FROM actividad WHERE email = 'test1@example.com')),
('Roberto Gómez', 'El año pasado fue increíble, no me lo pierdo este año', '2025-05-15 09:20:00', (SELECT id FROM actividad WHERE email = 'test1@example.com')),

('Ana Torres', '¡Increíble! Por fin tecnología específica para gatos', '2025-05-18 14:25:00', (SELECT id FROM actividad WHERE email = 'test2@example.com')),
('Carlos Ruiz', 'Me interesa mucho ver los robots alimentadores', '2025-05-19 11:10:00', (SELECT id FROM actividad WHERE email = 'test2@example.com')),

('Laura González', '¿Los gatos realmente participan en competencias?', '2025-05-20 16:35:00', (SELECT id FROM actividad WHERE email = 'test3@example.com')),
('Pablo Muñoz', 'Mi gato es muy ágil, ¡participaremos!', '2025-05-22 13:15:00', (SELECT id FROM actividad WHERE email = 'test3@example.com')),

('Carmen López', 'Las fotos del año pasado fueron hermosas', '2025-05-15 20:40:00', (SELECT id FROM actividad WHERE email = 'test4@example.com')),
('Diego Martínez', '¿Se pueden llevar cámaras profesionales?', '2025-05-17 17:50:00', (SELECT id FROM actividad WHERE email = 'test4@example.com')),

('Sofía Castro', 'Me encanta la danza contemporánea, será fascinante', '2025-05-23 19:30:00', (SELECT id FROM actividad WHERE email = 'test5@example.com')),

('Pedro Sánchez', '¿Habrá transmisión en vivo de las charlas?', '2025-05-24 12:20:00', (SELECT id FROM actividad WHERE email = 'test6@example.com')),
('Elena Vargas', 'Me interesan las charlas sobre comportamiento felino', '2025-05-24 15:45:00', (SELECT id FROM actividad WHERE email = 'test6@example.com')),

('Miguel Ángel', '¿Cuánto cuesta la entrada a la convención?', '2025-05-20 10:05:00', (SELECT id FROM actividad WHERE email = 'test7@example.com')),
('Isabella Rojas', 'Vendré desde Valparaíso, ¡no me lo pierdo!', '2025-05-21 14:30:00', (SELECT id FROM actividad WHERE email = 'test7@example.com')),

('Valentina Díaz', 'Excelente iniciativa para discutir políticas de protección', '2025-05-19 16:15:00', (SELECT id FROM actividad WHERE email = 'test8@example.com')),
('Fernando Pinto', '¿Qué autoridades participarán en el debate?', '2025-05-22 11:25:00', (SELECT id FROM actividad WHERE email = 'test8@example.com'));