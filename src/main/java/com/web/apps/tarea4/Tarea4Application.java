package com.web.apps.tarea4;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.MediaType;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.*;

@Controller
@SpringBootApplication
public class Tarea4Application {

    @Autowired
    private ActivityRepository activityRepository;

    @GetMapping("/")
    public String indexPage(Model model) {
        model.addAttribute("activitiesHtml", renderActivitiesHtml(1, 5));
        return "index";
    }

    @PostMapping(value = "/api/activities/paginated", produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Object> getPaginatedActivities(@RequestParam("page") int page) {
        int pageSize = 5;
        int totalActivities = activityRepository.getTotalActivities();
        int totalPages = (int) Math.ceil((double) totalActivities / pageSize);
        String html = renderActivitiesHtml(page, pageSize);
        Map<String, Object> resp = new HashMap<>();
        resp.put("totalPages", totalPages);
        resp.put("currentPage", page);
        resp.put("html", html);
        return resp;
    }

    @PostMapping("/api/activities/score")
    @ResponseBody
    public ResponseEntity<?> updateScore(@RequestParam("id") int id, @RequestParam("score") int score) {
        if (score < 1 || score > 7) {
            return ResponseEntity.badRequest().body("El puntaje debe ser un entero entre 1 y 7");
        }
        double avg = activityRepository.addScoreAndGetAverage(id, score);
        String avgStr = (avg == (int) avg) ? String.valueOf((int) avg) : String.format("%.1f", avg);
        return ResponseEntity.ok(Collections.singletonMap("score", avgStr));
    }

    private String renderActivitiesHtml(int page, int pageSize) {
        int offset = (page - 1) * pageSize;
        List<Map<String, Object>> activities = activityRepository.getActivities(pageSize, offset);
        StringBuilder sb = new StringBuilder();
        for (Map<String, Object> act : activities) {
            int id = (int) act.get("id");
            String inicio = String.valueOf(act.get("dia_hora_inicio"));
            String termino = act.get("dia_hora_termino") != null ? String.valueOf(act.get("dia_hora_termino")) : "-";
            String comuna = String.valueOf(act.get("comuna"));
            String sector = String.valueOf(act.get("sector"));
            String nombre = String.valueOf(act.get("nombre"));
            String temas = String.valueOf(act.get("temas"));
            int fotos = act.get("fotos") != null ? ((Number)act.get("fotos")).intValue() : 0;
            Object scoreObj = act.get("score");
            String scoreStr;
            if (scoreObj instanceof Double) {
                double s = (Double) scoreObj;
                scoreStr = (s == (int) s) ? String.valueOf((int) s) : String.format("%.1f", s);
            } else {
                scoreStr = String.valueOf(scoreObj);
            }
            sb.append("<tr>");
            sb.append("<td>" + inicio + "</td>");
            sb.append("<td>" + termino + "</td>");
            sb.append("<td>" + comuna + "</td>");
            sb.append("<td>" + sector + "</td>");
            sb.append("<td>" + temas + "</td>");
            sb.append("<td>" + nombre + "</td>");
            sb.append("<td>" + (fotos > 0 ? fotos : "-") + "</td>");
            sb.append("<td class='activity-score' data-id='" + id + "'>" + (scoreStr.equals("0") ? "-" : scoreStr) + "</td>");
            sb.append("<td><button class='evaluate-btn' data-id='" + id + "'>Evaluar</button></td>");
            sb.append("</tr>");
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        SpringApplication.run(Tarea4Application.class, args);
    }
}
