import { useState } from "react";

const Loading = () => {
  return (
    <div class="progress mt-4 mb-3">
      <div
        class="progress-bar progress-bar-striped progress-bar-animated bg-primary "
        role="progressbar"
        aria-label="Animated striped example"
        aria-valuenow="100"
        aria-valuemin="0"
        aria-valuemax="100"
        style={{ width: "100%" }}
      >
        Procesando Solicitud
      </div>
    </div>
  );
};

function AnalisisPasoUno() {
  const upload_url = "http://localhost:5000/upload-tres";
  const url_paso_dos = "http://localhost:5000/analizar-imagen-rn";
  const [selectedImage, setSelectedImage] = useState(null);

  const [imagenes, setImagenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mostrarResultados, setMostrarResultados] = useState(false);
  const [resultadoAnalisis, setResultadoAnalisis] = useState(null);
  const [opcionSeleccionada, setOpcionSeleccionada] = useState(null);
  const [archivoImagenSeleccionada, setArchivoImagenSeleccionada] =
    useState(null);

  const reinit = () => {
    setSelectedImage(null);
    setImagenes([]);
    setMostrarResultados(false);
    setResultadoAnalisis(null);
    setOpcionSeleccionada(null);
    setArchivoImagenSeleccionada(null);
  };

  const analizarImagen = async (opcion) => {
    setLoading(true);
    setResultadoAnalisis(null);
    const payload = {
      archivo_imagen: archivoImagenSeleccionada,
      rango_x: opcion,
    };
    try {
      const res = await fetch(url_paso_dos, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setResultadoAnalisis(data.analisis);
      console.log(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const uploadImage = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("myImage", selectedImage);
    formData.append("rgbColor", "rgbColor");
    try {
      const res = await fetch(upload_url, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log(data);

      setImagenes(data.links_imagenes);
      setArchivoImagenSeleccionada(data.jpg_original);
      setMostrarResultados(true);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Análisis de Imagenes</h1>
      {loading && <Loading />}
      <button className="btn btn-warning" onClick={reinit}>
        Reiniciar{" "}
      </button>
      {!mostrarResultados && (
        <>
          <div className="row">
            <div className="col-6">
              <div class="input-group mb-3">
                <input
                  type="file"
                  name="myImage"
                  class="form-control"
                  onChange={(event) => {
                    console.log(event.target.files[0]);
                    setSelectedImage(event.target.files[0]);
                  }}
                />
              </div>
            </div>
          </div>
          {selectedImage && (
            <div className="row">
              <div className="col-6">
                <img
                  alt="not fount"
                  width={"500px"}
                  src={URL.createObjectURL(selectedImage)}
                />
              </div>
              <div className="col-6">
                <button
                  className="btn btn-danger"
                  onClick={() => setSelectedImage(null)}
                >
                  Eliminar
                </button>
                <button class="btn btn-secondary" onClick={uploadImage}>
                  Analizar
                </button>
              </div>
            </div>
          )}
        </>
      )}
      <div class="row align-items-start">
        {mostrarResultados &&
          imagenes.map((imagen) => (
            <div className="col">
              <div class="card text-center" key={imagen.link}>
                <img
                  src={"http://localhost:5000/" + imagen.link}
                  class="card-img-top"
                  alt="{imagen.link}"
                />
                <div class="card-body">
                  <h5 class="card-title">
                    análisis preliminar opción {imagen.opcion_analisis + 1}
                  </h5>
                  <p class="card-text">
                    {" "}
                    Ley de Cobre:{" "}
                    <span className="fw-semibold">
                      {imagen.ley_cobre}%
                    </span>{" "}
                  </p>
                  {(imagen.opcion_analisis === opcionSeleccionada && (
                    <button
                      className="btn btn-primary"
                      onClick={() => {
                        setOpcionSeleccionada(imagen.opcion_analisis);
                        analizarImagen(imagen.opcion_analisis);
                      }}
                    >
                      Procesar Usando esta Opción
                    </button>
                  )) || (
                    <button
                      className="btn btn-outline-secondary"
                      onClick={() => {
                        setOpcionSeleccionada(imagen.opcion_analisis);
                        analizarImagen(imagen.opcion_analisis);
                      }}
                    >
                      Procesar Usando esta Opción
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
      </div>
      {loading && <Loading />}

      {opcionSeleccionada !== null && (
        <div className="row mt-4">
          <div className="col">
            {resultadoAnalisis && (
              <div class="card  text-center">
                <img
                  src={
                    "http://localhost:5000/" + resultadoAnalisis.imagen_original
                  }
                  class="card-img-top"
                  alt="{resultadoAnalisis.imagen_original}"
                />
                <div class="card-body">
                  <h5 class="card-title">Imagen Original</h5>
                  <p class="card-text">
                    Opción de Análisis:{" "}
                    <span className="fw-semibold">
                      {resultadoAnalisis.opcion_analisis + 1}
                    </span>{" "}
                  </p>
                </div>
              </div>
            )}
          </div>
          <div className="col">
            {resultadoAnalisis && (
              <div class="card  text-center">
                <img
                  src={"http://localhost:5000/" + resultadoAnalisis.link}
                  class="card-img-top"
                  alt="{resultadoAnalisis.link}"
                />
                <div class="card-body">
                  <h5 class="card-title">
                    Resultado del Análisis de la Imagen
                  </h5>
                  <p class="card-text">
                    {" "}
                    Ley de Cobre:{" "}
                    <span className="fw-semibold">
                      {resultadoAnalisis.ley_cobre}%
                    </span>{" "}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalisisPasoUno;
