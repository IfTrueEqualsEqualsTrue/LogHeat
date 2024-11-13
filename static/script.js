let plotInterval;

        document.addEventListener('DOMContentLoaded', (event) => {
            fetch('/get_com_ports')
                .then(response => response.json())
                .then(data => {
                    const dropdownMenu = document.getElementById('dropdownMenu');
                    data.ports.forEach(port => {
                        const option = document.createElement('option');
                        option.value = port;
                        option.text = port;
                        dropdownMenu.add(option);
                    });
                });

            fetchPlotData();
            plotInterval = setInterval(fetchPlotData, 50);  // Fetch plot data every 50 milliseconds
        });

        function toggleState() {
            fetch('/toggle', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    const button = document.getElementById('startButton');
                    if (data.state) {
                        button.textContent = 'Stop saving';
                        startPlotUpdate();
                    } else {
                        button.textContent = 'Start saving';
                        stopPlotUpdate();
                    }
                    console.log('State:', data.state);
                });
        }

        function updateComPort() {
            const selectedPort = document.getElementById('dropdownMenu').value;
            fetch('/update_com_port', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ port: selectedPort })
            })
            .then(response => response.json())
            .then(data => {
                console.log('COM Port updated to:', data.port);
            });
        }

        function startPlotUpdate() {
            plotInterval = setInterval(fetchPlotData, 50);  // Update plot every 50ms
        }

        function stopPlotUpdate() {
            clearInterval(plotInterval);
        }

        async function fetchPlotData() {
            const response = await fetch('/plot_data');
            const plotData = await response.json();
            Plotly.react('plot', plotData.data, plotData.layout);
        }