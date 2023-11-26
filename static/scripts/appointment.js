// script.js

function handleInput() {
    // Reset the display when the name is changed
    document.getElementById('additional-fields').style.display = 'none';
    document.getElementById('region-label').style.display = 'none';
    document.getElementById('topic-label').style.display = 'none';
    document.getElementById('availability-button').style.display = 'none';

    // Hide the available machines list
    document.getElementById('available-machines').style.display = 'none';

    // Hide the machine data table and clear its content
    document.getElementById('table-container').style.display = 'none';
    document.getElementById('table-container').innerHTML = '';

    var search = document.getElementById('name').value;
    var dropdown = document.getElementById('name-list');

    if (search.length >= 2) {
        fetch('/autocomplete?search=' + search)
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            });
    } else {
        dropdown.style.display = 'none';
    }
}

function handleButtonClick() {
    // Trigger the same functionality as clicking in the name
    handleInput();
}

function displayResults(results) {
    var dropdown = document.getElementById('name-list');
    dropdown.innerHTML = '';

    results.forEach(function (name) {
        var listItem = document.createElement('li');
        listItem.textContent = name;
        listItem.onclick = function () {
            document.getElementById('name').value = name;
            fetchUserInfo(name);
            dropdown.style.display = 'none';

            // Show the additional fields and labels
            document.getElementById('additional-fields').style.display = 'block';
            document.getElementById('region-label').style.display = 'block';
            document.getElementById('topic-label').style.display = 'block';

            // Show the button
            document.getElementById('availability-button').style.display = 'block';
        };
        dropdown.appendChild(listItem);
    });

    dropdown.style.display = 'block';
}

function fetchUserInfo(name) {
    fetch('/patient_info?name=' + name)
        .then(response => response.json())
        .then(data => {
            document.getElementById('region').value = data.region || '';
            document.getElementById('topic').value = data.ntfy_topic || '';
        });
}

function checkAvailability() {
    var name = document.getElementById('name').value;

    fetch('/check_availability?name=' + name)
        .then(response => response.json())
        .then(data => {
            displayAvailableMachines(data.available_machines);
        });
}

function displayAvailableMachines(availableMachines) {
    var availableMachinesList = document.getElementById('available-machines');
    availableMachinesList.innerHTML = '';

    if (availableMachines.length > 0) {
        availableMachines.forEach(function (machine) {
            var listItem = document.createElement('li');
            var link = document.createElement('a');
            link.textContent = machine;
            link.href = '#';  // Set href to '#' to prevent the page from navigating
            link.onclick = function () {
                showMachineTable(machine);
            };
            listItem.appendChild(link);
            availableMachinesList.appendChild(listItem);
        });

        // Show the list of available machines
        availableMachinesList.style.display = 'block';
    } else {
        // If no machines are available, hide the list
        availableMachinesList.style.display = 'none';
    }
}

function showMachineTable(machine) {
    // Fetch data for the patient and machine
    var name = document.getElementById('name').value;

    fetch('/patient_info?name=' + name)
        .then(response => response.json())
        .then(patientData => {
            fetch('/machine_info?machine=' + machine)
                .then(response => response.json())
                .then(machineData => {
                    fetch('/treatment_info?machine=' + machine +"&name=" + name)
                        .then(response => response.json())
                        .then(treatmentData => {
                            // Create and display the table
                            createAndDisplayTable(patientData, machineData,treatmentData);
                        });
                });
        });
}

function createAndDisplayTable(patientData, machineData,treatmentData) {
    var tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = '';  // Clear previous content

    // Create the table element
    var table = document.createElement('table');
    table.border = '1';

    // Create the table header
    var headerRow = table.insertRow();
    var patientHeader = headerRow.insertCell(0);
    patientHeader.textContent = 'Patient Data';
    patientHeader.colSpan = 2;

    var machineHeader = headerRow.insertCell(1);
    machineHeader.textContent = 'Machine Data';
    machineHeader.colSpan = 2;

    // Create the table rows
    var dataRow = table.insertRow();
    createCell(dataRow, 'Patient Name:', patientData.full_name);
    createCell(dataRow, 'Type of cancer:', patientData.region);
    createCell(dataRow, 'Treatment duration:', patientData.duration + " min");
    createCell(dataRow, 'Number of fractions:', patientData.fractions);


    var machineDataRow = table.insertRow();
    createCell(machineDataRow, 'Machine Name:', machineData.name);
    createCell(machineDataRow, 'Machine Type:', machineData.full_name );
    createCell(machineDataRow, "Available date and hour",treatmentData.slots)
    createCell(machineDataRow, "Bookable",treatmentData.bookable)

    // Append the table to the container
    tableContainer.appendChild(table);

    // Show the table
    tableContainer.style.display = 'block';
}

function createCell(row, label, value) {
    var cellLabel = row.insertCell();
    cellLabel.textContent = label;

    var cellValue = row.insertCell();
    cellValue.textContent = value;
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('#name')) {
        var dropdown = document.getElementById('name-list');
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        }
    }
};
