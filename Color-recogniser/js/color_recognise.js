function hexToRgb(hex) {
    let bigint = parseInt(hex.substring(1), 16);
    return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
}

function euclideanDistance(color1, color2) {
    return Math.sqrt(
        Math.pow(color1[0] - color2[0], 2) +
        Math.pow(color1[1] - color2[1], 2) +
        Math.pow(color1[2] - color2[2], 2)
    );
}

function findClosestColor(rgb) {
    let closestColor = colorData[0].name;
    let minDistance = Infinity;
    colorData.forEach(color => {
        let distance = euclideanDistance(rgb, color.rgb);
        if (distance < minDistance) {
            minDistance = distance;
            closestColor = color.name;
        }
    });
    return closestColor;
}

function updatePrediction() {
    let selectedColor = document.getElementById("color-picker").value;
    let rgb = hexToRgb(selectedColor);
    document.getElementById("color-display").style.backgroundColor = selectedColor;
    document.getElementById("color-name").textContent = findClosestColor(rgb);
}

document.getElementById("color-picker").addEventListener("input", updatePrediction);

function displayPredefinedColors() {
    const container = document.getElementById("predefined-colors");
    container.innerHTML = "";
    colorData.forEach((color, index) => {
        const colorBox = document.createElement("div");
        colorBox.className = "color-box";
        colorBox.innerHTML = `
            <div class="color-preview" style="background-color: rgb(${color.rgb.join(",")})"></div>
            <input class="color-name-input" type="text" value="${color.name}" onchange="editColorName(${index}, this.value)">
            <span class="color-text">RGB: ${color.rgb.join(", ")}</span>
            <button onclick="removeColor(${index})">X</button>
        `;
        container.appendChild(colorBox);
    });
}

function editColorName(index, newName) {
    colorData[index].name = newName;
    updatePrediction();
}

function removeColor(index) {
    colorData.splice(index, 1);
    displayPredefinedColors();
    updatePrediction();
}

function addNewColor() {
    let newColorHex = document.getElementById("new-color-picker").value;
    let newColorName = document.getElementById("new-color-name").value.trim();
    if (newColorName) {
        colorData.push({ name: newColorName, rgb: hexToRgb(newColorHex) });
        displayPredefinedColors();
        updatePrediction();
    }
}

displayPredefinedColors();