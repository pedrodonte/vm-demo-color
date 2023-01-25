import { useState } from "react";
function UploadImage() {
  const upload_url = "http://localhost:5000/upload";
  const [selectedImage, setSelectedImage] = useState(null);
  const [rgbColor, setRgbColor] = useState(null);
  const [imagenResult, setImagenResult] = useState(null);
  const [rango_hsv, setRango_hsv] = useState(null);

  const uploadImage = async () => {
    const formData = new FormData();
    formData.append("myImage", selectedImage);
    formData.append("rgbColor", rgbColor);
    try {
      const res = await fetch(upload_url, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log(data);
      setImagenResult(data.image_url);
      setRango_hsv(data.rango_hsv);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Upload and Display Image usign React Hook's</h1>

      <br />
      <br />
      <input
        type="file"
        name="myImage"
        onChange={(event) => {
          console.log(event.target.files[0]);
          setSelectedImage(event.target.files[0]);
        }}
      />
      <br />
      {selectedImage && (
        <div>
          <br />
          <button
            onClick={() => {
              const canvas = document.getElementById("canvas");

              const ctx = canvas.getContext("2d");
              const img = new Image();
              img.onload = function () {
                ctx.drawImage(img, 0, 0);
              };
              img.src = URL.createObjectURL(selectedImage);

              // Añadir evento para extraer pixel
              canvas.addEventListener("mousemove", (e) => {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const pixel = ctx.getImageData(x, y, 1, 1);
                const data = pixel.data;
                const rgba = `rgba(${data[0]}, ${data[1]}, ${data[2]}, ${data[3]})`;

                document.getElementById("hovered-color").style.backgroundColor =
                  rgba;
              });

              // Añadir evento para extraer pixel al hacer click
              canvas.addEventListener("click", (e) => {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const pixel = ctx.getImageData(x, y, 1, 1);
                const data = pixel.data;
                const rgba = `rgba(${data[0]}, ${data[1]}, ${data[2]}, ${data[3]})`;
                document.getElementById(
                  "selected-color"
                ).style.backgroundColor = rgba;
                setRgbColor(`${data[0]},${data[1]},${data[2]}`);
              });
            }}
          >
            Empezar el proceso
          </button>
        </div>
      )}
      <table>
        <thead>
          <tr>
            <th>Original</th>
            <th>Pre Color</th>
            <th>Color</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <canvas id="canvas" width="500" height="500"></canvas>
            </td>
            <td class="color-cell" id="hovered-color"></td>
            <td class="color-cell" id="selected-color">
              {rgbColor}
              <button onClick={uploadImage}>Upload</button>
            </td>
            <td>
              {imagenResult && (
                <>
                  <img
                    alt="not fount"
                    width={"500px"}
                    src={"http://localhost:5000/" + imagenResult}
                  />
                  Rango HSV:{rango_hsv}
                </>
              )}
            </td>
          </tr>
        </tbody>
      </table>
      <br />
    </div>
  );
}

export default UploadImage;
