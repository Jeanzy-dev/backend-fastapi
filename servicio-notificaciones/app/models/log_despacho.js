class LogDespachoCorreo {
    constructor({ id_log, id_envio, proveedor_smtp = 'Gmail SMTP', id_mensaje_servidor, intentos = 1, detalle_respuesta, estado = 1 }) {
        this.id_log = id_log;
        this.id_envio = id_envio;
        this.proveedor_smtp = proveedor_smtp;
        this.id_mensaje_servidor = id_mensaje_servidor;
        this.intentos = intentos;
        this.detalle_respuesta = detalle_respuesta;
        this.estado = estado;
    }
}

module.exports = LogDespachoCorreo;