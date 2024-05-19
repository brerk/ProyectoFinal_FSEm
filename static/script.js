// async function handleLightSlideBar() {
//     // Handle light toggle
//     try {
//         let response = await fetch('/control_light', {
//             method: 'post'
//         });
//
//         if (response.ok) {
//             let data = await response.json();
//             let lightstate = data.light_state ? 'on' : 'off';
//             document.getelementbyid('light-status').textcontent = 'light is ' + lightstate;
//             alert('light toggled! light is now ' + lightstate);
//         } else {
//             alert('failed to toggle light.');
//         }
//
//     } catch (error) {
//         console.error('error:', error);
//         alert('failed to toggle light due to network error.');
//     }
// }

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
