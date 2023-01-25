import imagen from "./assets/roberto.jpg";
import { useEffect, useState } from "react";
function App() {
  // useState for rgbColor
  const [rgbColor, setRgbColor] = useState(null);

  const cargarImagen = () => {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();

    console.log("imagen cargando");
    img.src = imagen;
    //"https://2j70j0vn5g.execute-api.us-east-2.amazonaws.com/default/8ed98e3958754b95aa0d84c3025a31bb_original.jpg";
    img.onload = () => {
      console.log("imagen cargada");
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };

    // Añadir evento para extraer pixel
    canvas.addEventListener("mousemove", (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const pixel = ctx.getImageData(x, y, 1, 1);
      const data = pixel.data;
      const rgba = `rgba(${data[0]}, ${data[1]}, ${data[2]}, ${data[3]})`;
      setRgbColor(rgba);
      document.getElementById("hovered-color").style.backgroundColor = rgba;
    });

    // Añadir evento para extraer pixel al hacer click
    canvas.addEventListener("click", (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const pixel = ctx.getImageData(x, y, 1, 1);
      const data = pixel.data;
      const rgba = `rgba(${data[0]}, ${data[1]}, ${data[2]}, ${data[3]})`;
      document.getElementById("selected-color").style.backgroundColor = rgba;
    });
  };

  useEffect(() => {
    cargarImagen();
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Hovered color</th>
          <th>Selected color</th>
          <th>imagen</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <canvas id="canvas" width="500" height="500"></canvas>
          </td>
          <td class="color-cell" id="hovered-color"></td>
          <td class="color-cell" id="selected-color"></td>
          <td>
            {" "}
            <button
              onClick={() => {
                cargarImagen();
              }}
            >
              Dibujar imagen
            </button>
            {rgbColor}
          </td>
        </tr>
      </tbody>
    </table>
  );
}

export default App;
