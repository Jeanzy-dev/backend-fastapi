class EnvioAlerta {
    constructor({ id_envio, id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho = 'PENDIENTE', estado = 1 }) {
        this.id_envio = id_envio;
        this.id_plantilla = id_plantilla;
        this.documento_estudiante = documento_estudiante;
        this.nombre_estudiante = nombre_estudiante;
        this.correo_destinatario = correo_destinatario;
        this.total_tardanzas = total_tardanzas;
        this.codigo_seguimiento = codigo_seguimiento;
        this.estado_despacho = estado_despacho;
        this.estado = estado;
    }
}

module.exports = EnvioAlerta;