package com.group2.incidentservice.api.controller;

import java.util.List;

import com.group2.incidentservice.api.dto.HistorialIncidenteWithTypeDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.group2.incidentservice.api.dto.IncidentWithTypeDTO;
import com.group2.incidentservice.api.dto.UpdateEstadoSistemaDTO;
import com.group2.incidentservice.application.service.IncidentService;
import com.group2.incidentservice.domain.model.Incident;
import com.group2.incidentservice.domain.model.HistorialIncidente;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.MalformedURLException;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
@RequestMapping("/api/incidents")
public class IncidentController {

    @Autowired
    private IncidentService incidentService;

    @PostMapping
    public ResponseEntity<Incident> createIncident(@RequestBody Incident incident) {
        Incident createdIncident = incidentService.createIncident(incident);
        return ResponseEntity.ok(createdIncident);
    }

    @GetMapping
    public ResponseEntity<List<Incident>> getAllIncidents() {
        List<Incident> incidents = incidentService.getAllIncidents();
        return ResponseEntity.ok(incidents);
    }

    @GetMapping("/with-type")
    public ResponseEntity<List<IncidentWithTypeDTO>> getAllIncidentsWithType() {
        List<IncidentWithTypeDTO> incidents = incidentService.getAllIncidentsWithType();
        return ResponseEntity.ok(incidents);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Incident> getIncidentById(@PathVariable Integer id) {
        Incident incident = incidentService.getIncidentById(id);
        return ResponseEntity.ok(incident);
    }

    @GetMapping("/{id}/with-type")
    public ResponseEntity<IncidentWithTypeDTO> getIncidentWithTypeById(@PathVariable Integer id) {
        IncidentWithTypeDTO incident = incidentService.getIncidentWithTypeById(id);
        return ResponseEntity.ok(incident);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Incident> updateIncident(@PathVariable Integer id, @RequestBody Incident incident) {
        Incident updatedIncident = incidentService.updateIncident(id, incident);
        return ResponseEntity.ok(updatedIncident);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteIncident(@PathVariable Integer id) {
        incidentService.deleteIncident(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{id}/confirm")
    public ResponseEntity<Void> confirmIncident(@PathVariable Integer id) {
        incidentService.confirmIncident(id);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/{id}/reject")
    public ResponseEntity<Void> rejectIncident(@PathVariable Integer id) {
        incidentService.rejectIncident(id);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/historial/{id}")
    public ResponseEntity<Void> deleteHistorialIncident(@PathVariable Integer id) {
        incidentService.deleteHistorialIncident(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/historial")
    public ResponseEntity<List<HistorialIncidente>> getAllHistorialIncidentes() {
        List<HistorialIncidente> historial = incidentService.getAllHistorialIncidentes();
        return ResponseEntity.ok(historial);
    }

    @GetMapping("/historial/{id}")
    public ResponseEntity<HistorialIncidente> getHistorialIncidenteById(@PathVariable Integer id) {
        HistorialIncidente historial = incidentService.getHistorialIncidenteById(id);
        return ResponseEntity.ok(historial);
    }

    @PutMapping("/historial/{id}/estado")
    public ResponseEntity<Void> updateHistorialEstadoSistema(
            @PathVariable Integer id,
            @RequestBody UpdateEstadoSistemaDTO updateDTO) {
        incidentService.updateHistorialEstadoSistema(id, updateDTO.estadoSistema());
        return ResponseEntity.ok().build();
    }
    @GetMapping("/historial/with-type")
    public ResponseEntity<List<HistorialIncidenteWithTypeDTO>> getAllHistorialIncidentesWithType() {
        List<HistorialIncidenteWithTypeDTO> historial = incidentService.getAllHistorialIncidentesWithType();
        return ResponseEntity.ok(historial);
    }

    @GetMapping("/historial/{id}/with-type")
    public ResponseEntity<HistorgtiialIncidenteWithTypeDTO> getHistorialIncidenteWithTypeById(@PathVariable Integer id) {
        HistorialIncidenteWithTypeDTO historial = incidentService.getHistorialIncidenteWithTypeById(id);
        return ResponseEntity.ok(historial);
    }
    @GetMapping("/image/{filename:.+}")
    public ResponseEntity<Resource> getImage(@PathVariable String filename) {
        Path imagePath = Paths.get("ruta/a/tu/carpeta/imagenes", filename);

        try {
            Resource resource = new UrlResource(imagePath.toUri());
            if (resource.exists() || resource.isReadable()) {
                return ResponseEntity.ok()
                        .contentType(MediaType.IMAGE_JPEG)
                        .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
