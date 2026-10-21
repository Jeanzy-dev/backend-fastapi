class PlantillaNotificacion {
    constructor({ id_plantilla, codigo_plantilla, asunto, cuerpo_html, estado = 1 }) {
        this.id_plantilla = id_plantilla;
        this.codigo_plantilla = codigo_plantilla;
        this.asunto = asunto;
        this.cuerpo_html = cuerpo_html;
        this.estado = estado;
    }
}

module.exports = PlantillaNotificacion;