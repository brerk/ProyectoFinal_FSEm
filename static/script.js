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
