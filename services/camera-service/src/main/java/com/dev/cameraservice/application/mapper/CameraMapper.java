package com.dev.cameraservice.application.mapper;

import com.dev.cameraservice.api.dto.CameraRequestDTO;
import com.dev.cameraservice.api.dto.CameraResponseDTO;
import com.dev.cameraservice.domain.model.Camera;
import org.springframework.stereotype.Component;

@Component
public class CameraMapper {

    public Camera toModel(CameraRequestDTO dto) {
        Camera camera = new Camera();
        camera.setName(dto.name());
        camera.setDescription(dto.description());
        camera.setLocation(dto.location());
        camera.setUrlStream(dto.urlStream());
        camera.setStatus("activo");
        //camera.setCreatedAt(java.time.LocalDateTime.now());
        //camera.setUpdatedAt(java.time.LocalDateTime.now());
        return camera;
    }

    public CameraResponseDTO toResponseDTO(Camera camera) {
        return new CameraResponseDTO(
                camera.getId(),
                camera.getName(),
                camera.getDescription(),
                camera.getLocation(),
                camera.getUrlStream(),
                camera.getStatus(),
                camera.getCreatedAt() != null ? camera.getCreatedAt().toString() : null,
                camera.getUpdatedAt() != null ? camera.getUpdatedAt().toString() : null
        );
    }

}
