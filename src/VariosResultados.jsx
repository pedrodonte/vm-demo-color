import { useState } from "react";
function VariosResultados() {
  const upload_url = "http://localhost:5000/upload-tres";
  const [selectedImage, setSelectedImage] = useState(null);

  const [imagenes, setImagenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mostrarResultados, setMostrarResultados] = useState(false);

  const reinit = () => {
    setSelectedImage(null);
    setImagenes([]);
    setMostrarResultados(false);
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
      setMostrarResultados(true);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Análisis de Imagenes</h1>
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
                {loading && (
                  <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {mostrarResultados &&
        imagenes.map((imagen) => (
          <div className="row" key={imagen}>
            <div className="col-6">
              <img
                alt="not fount"
                width={"500px"}
                src={"http://localhost:5000/" + imagen}
              />
            </div>
            <div className="col-6">
              <img
                alt="not fount"
                width={"500px"}
                src={URL.createObjectURL(selectedImage)}
              />
            </div>
          </div>
        ))}
    </div>
  );
}

export default VariosResultados;
