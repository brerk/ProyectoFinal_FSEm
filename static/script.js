// scrtips.js: Controls dinamic elements from web interface
// Copyright (C) 2024  Erik Bravo
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

async function handleLightSlideBar(value){
    console.log(value)

    if (value < 0){
        value = 0;
    }
    else if (value > 100) {
        value = 100;
    }

    try {
        let response = await fetch('/control_light', {
            method: 'POST',
            headers :{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ value: parseInt(value) })
        });

        if (response.ok) {
            let data = await response.json();
            let lightValue = data.light_power

            document.getElementById('lightPowerValue').innerHTML = lightValue;
        } else {
            alert('failed to change light value.');
        }

    } catch (error) {
        console.error('error:', error);
        alert('failed to toggle light due to network error.');
    }
}

async function handleFanSlideBar(value){
    console.log(value)
    try {
        let response = await fetch('/control_fan', {
            method: 'POST',
            headers :{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ value: parseInt(value) })
        });

        if (response.ok) {
            let data = await response.json();
            let fanSpeed = data.fan_speed

            document.getElementById('fan_speed').innerHTML = fanSpeed;
        } else {
            alert('failed to change light value.');
        }

    } catch (error) {
        console.error('error:', error);
        alert('failed to toggle fan speed due to network error.');
    }
}

function validateForm(event) {
    console.log(event);

    var hourminute = document.forms["irrigation_form"]["hourminute"].value;
    var duration = document.forms["irrigation_form"]["duration"].value;
    var min_temp = document.forms["irrigation_form"]["min_temp"].value;
    var max_temp = document.forms["irrigation_form"]["max_temp"].value;

    console.log(duration);


    if (hourminute == "") {
        alert("An hour:minute must be specified.");

        event.preventDefault()
        return false;
    }

    if (duration == "" || min_temp == "" || max_temp == "") {
        console.log(duration);
        alert("All input field must be filled out.");

        event.preventDefault()
        return false;
    }

    return true;
}

function validateTempsForm(event) {
    console.log(event);

    var min_temp = document.forms["temps_form"]["min_temp"].value;
    var max_temp = document.forms["temps_form"]["max_temp"].value;

    console.log(min_temp);


    if (min_temp == "" || max_temp == "") {
        alert("All input field must be filled out.");

        event.preventDefault()
        return false;
    }

    if (parseInt(min_temp) >= parseInt(max_temp)) {
        alert("Invalid temperatures, make sure min_temp is not higuer or equal to max_temp.");

        event.preventDefault()
        return false;
    }

    return true;
}

function validateWantedTempForm(event) {
    console.log(event);

    var wanted_temp = document.forms["temps_form"]["wanted_temp"].value;

    if (wanted_temp == "") {
        alert("All input field must be filled out.");

        event.preventDefault()
        return false;
    }

    return true;
}

function actualizarImagen() {
    const numeroAleatorio = Math.floor(Math.random() * 1000);
    const nuevaUrlImagen = `/static/temps.jpg?cache=${numeroAleatorio}`;

    document.getElementById('temps-graph').src = nuevaUrlImagen;
}

setInterval(actualizarImagen, 10000);
