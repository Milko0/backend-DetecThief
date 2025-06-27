package com.group2.incidentservice.domain.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class HistorialIncidente {
    private Integer id;
    private Integer incidenteId;
    private String comentario;
    private LocalDateTime fechaCambio;
    private String contactosNotificados;
    private String estadoSistema;
}