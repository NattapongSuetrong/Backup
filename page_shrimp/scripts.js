//switch button1
const toggleSwitch1 = document.getElementById("switch1");
const toggleStatus1 = document.getElementById("switch-status1");

function onCheckboxToggle1() {
  const isChecked1 = this.hasAttribute("checked");

  /* 1. Update toggle switch visual state. */
  this.toggleAttribute("checked");

  /* 2. Update toggle switch status text. */
  toggleStatus1.innerText = isChecked1 ? "OFF" : "ON";
  if (isChecked1) {/* status switch1 */
    status_pump = "OFF"
    system(status_pump)
}
   else{
   status_pump = "ON"
   system(status_pump)
   }
   console.log("pump =",status_pump)
}
toggleSwitch1.addEventListener("change", onCheckboxToggle1);

//switch button2
const toggleSwitch2 = document.getElementById("switch2");
const toggleStatus2 = document.getElementById("switch-status2");

function onCheckboxToggle2() {
  const isChecked2 = this.hasAttribute("checked");

  /* 1. Update toggle switch visual state. */
  this.toggleAttribute("checked");

  /* 2. Update toggle switch status text. */
  toggleStatus2.innerText = isChecked2 ? "OFF" : "ON";

  //console.log("switch 2 =", !isChecked2); /* status switch2 */
  if (isChecked2) {
    status_light = "OFF"
    light(status_light)
}
   else{
   status_light = "ON"
   light(status_light)
   }
   console.log("light =",status_light)
}

toggleSwitch2.addEventListener("change", onCheckboxToggle2);

async function system(status) {
    await fetch(`http://localhost:8888/status/${status}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            if (status === 'ON') {
                alert('Pump started successfully');
            } else if (status === 'OFF') {
                alert('Pump stopped successfully');
            }
        } else {
            if (status === 'ON') {
                alert('Failed to start pump');
            } else if (status === 'OFF') {
                alert('Failed to stop pump');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (status === 'ON') {
            alert('Failed to start pump');
        } else if (status === 'OFF') {
            alert('Failed to stop pump');
        }
    });
}

async function light(lightStatus) {
    await fetch(`http://localhost:8888/light/${lightStatus}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            if (lightStatus === 'ON') {
                alert('Light started successfully');
            } else if (lightStatus === 'OFF') {
                alert('Light stopped successfully');
            }
        } else {
            if (lightStatus === 'ON') {
                alert('Failed to start light');
            } else if (lightStatus === 'OFF') {
                alert('Failed to stop light');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (lightStatus === 'ON') {
            alert('Failed to start light');
        } else if (lightStatus === 'OFF') {
            alert('Failed to stop light');
        }
    });
}
