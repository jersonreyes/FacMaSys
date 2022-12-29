function chartDefault(type,labels,data, LABEL_VALUE="LABEL", LABEL_TOTAL="1") {
    var options = {
        colors: ['#FB8C00', '#6D4C41', '#8E24AA', '#00ACC1', '#C0CA33'],
        chart: {
            redrawOnParentResize: true,
            toolbar: {
                show: true,
                offsetX: -240,
                offsetY: 5,
                tools: {
                download: true,
                selection: true,
                zoom: true,
                zoomin: true,
                zoomout: true,
                reset: false,
                pan: false,
                },
                export: {
                svg: {
                    filename: undefined,
                },
                png: {
                    filename: undefined,
                }
                },
                autoSelected: 'zoom'
            },
            zoom: { enabled: true },
            reset: { enabled: false },
            pan: { enabled: false },
            animations: { enabled: true },
            foreColor: "#000000",
            fontFamily: "sans-serif",
            type: type
        },

        // States
        states: {
            hover: {
                filter: {
                type: 'lighten',
                value: 0.04,
                },
            },
            active: {
                filter: {
                type: 'darken',
                value: 0.88,
                },
            },
        },

        // Fill
        fill: {
            opacity: 1,
            gradient: {
                type: 'vertical',
                shadeIntensity: 1,
                opacityFrom: 1,
                opacityTo: 0,
                stops: [0, 100],
            },
        },

        // Datalabels
        dataLabels: { enabled: false },

        // Stroke
        stroke: {
            width: 3,
            curve: 'smooth',
            lineCap: 'round',
        },

        // Grid
        grid: {
            strokeDashArray: 3,
            borderColor: "#000000",
            xaxis: {
                lines: {
                    show: false
                }
            },
        },

        series: [{
            name: 'sales',
            data: data,
        }],
        xaxis: {
            axisBorder: { show: false },
            axisTicks: { show: false },

            // Markers
            markers: {
            size: 0,
            strokeColors: "#000000",
            },

            // Tooltip
            tooltip: {
                x: {
                    show: false,
                },
            },
            categories: labels,
        },
        // Legend
        legend: {
            show: true,
            fontSize: String(13),
            position: 'top',
            horizontalAlign: 'right',
            markers: {
            radius: 12,
            },
            fontWeight: 500,
            itemMargin: { horizontal: 12 },
            labels: {
            colors: "#000000",
            },
        },
    
        // plotOptions
        plotOptions: {
            // Bar
            bar: {
            borderRadius: 4,
            distributed: true
            },
    
            // Pie + Donut
            pie: {
            donut: {
                labels: {
                show: true,
                value: LABEL_VALUE,
                total: LABEL_TOTAL,
                },
            },
            },
    
            // Radialbar
            radialBar: {
            track: {
                strokeWidth: '100%',
                background: "#000000",
            },
            dataLabels: {
                value: LABEL_VALUE,
                total: LABEL_TOTAL,
            },
            },
    
            // Radar
            radar: {
            polygons: {
                fill: { colors: ['transparent'] },
                strokeColors: "#000000",
                connectorColors: "#000000",
            },
            },
    
            // polarArea
            polarArea: {
            rings: {
                strokeColor: "#000000",
            },
            spokes: {
                connectorColors: "#000000",
            },
            },
        },

    }
    return options;
}