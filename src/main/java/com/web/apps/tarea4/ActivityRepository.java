package com.web.apps.tarea4;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

@Repository
public class ActivityRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public int getTotalActivities() {
        Integer total = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM actividad WHERE email LIKE 'test%'", Integer.class);
        return total != null ? total : 0;
    }

    public List<Map<String, Object>> getActivities(int pageSize, int offset) {
        return jdbcTemplate.queryForList(
            "SELECT a.id, a.dia_hora_inicio, a.dia_hora_termino, c.nombre AS comuna, a.sector, a.nombre, " +
            "COALESCE((SELECT GROUP_CONCAT(CASE WHEN t.tema = 'otro' AND t.glosa_otro IS NOT NULL AND t.glosa_otro != '' THEN t.glosa_otro ELSE t.tema END SEPARATOR ', ') FROM actividad_tema t WHERE t.actividad_id = a.id), '-') AS temas, " +
            "(SELECT COUNT(*) FROM foto f WHERE f.actividad_id = a.id) AS fotos, " +
            "COALESCE(ROUND((SELECT AVG(nota)*10 FROM nota WHERE actividad_id = a.id))/10, 0) AS score " +
            "FROM actividad a JOIN comuna c ON a.comuna_id = c.id WHERE a.email LIKE 'test%' ORDER BY a.id LIMIT ? OFFSET ?",
            pageSize, offset
        );
    }

    public double addScoreAndGetAverage(int actividadId, int score) {
        jdbcTemplate.update("INSERT INTO nota (actividad_id, nota) VALUES (?, ?)", actividadId, score);
        Double avg = jdbcTemplate.queryForObject("SELECT AVG(nota) FROM nota WHERE actividad_id = ?", Double.class, actividadId);
        return avg != null ? avg : score;
    }
}
