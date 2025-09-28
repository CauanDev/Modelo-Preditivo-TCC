import React, { useRef } from "react";
import Chart from "react-apexcharts";

const SexoBarChart = () => {
  const chartRef = useRef(null);

  const categorias = ["Ignorado", "Masculino", "Feminino"];

  // Percentuais normalizados
  const sobreviventes = [2, 48, 50]; // total 5232
  const obitoPrecoce = [1, 55, 44]; // total 9334

  const options = {
    chart: {
      id: "sexo-barras",
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "50%",
        dataLabels: {
          position: "top",
        },
      },
    },
    dataLabels: {
      enabled: true,
      offsetY: -40,
      style: { fontSize: "12px", colors: ["#00E396", "#FF4560"] },
      formatter: (val) => `${val}%`,
    },
    xaxis: {
      categories: categorias,
      title: { text: "Sexo" },
    },
    yaxis: {
      title: { text: "Percentual (%)" },
      min: 0,
      max: 100,
    },
    legend: {
      position: "top",
      horizontalAlign: "center",
      labels: { useSeriesColors: true },
    },
    colors: ["#00E396", "#FF4560"],
    title: { text: "Distribuição de Óbitos por Sexo", align: "center" },
  };

  const series = [
    { name: "Sobreviventes", data: sobreviventes },
    { name: "Óbito até 1 ano", data: obitoPrecoce },
  ];

  const handleDownload = async () => {
    if (chartRef.current) {
      const chartObj = chartRef.current.chart;
      const { imgURI } = await chartObj.dataURI();
      const link = document.createElement("a");
      link.href = imgURI;
      link.download = "sexo_barras_chart.png";
      link.click();
    }
  };

  return (
    <div>
      <Chart
        ref={chartRef}
        options={options}
        series={series}
        type="bar"
        height={400}
      />
      <button
        onClick={handleDownload}
        style={{ marginTop: 20, padding: "8px 16px" }}
      >
        Baixar Gráfico (PNG)
      </button>
    </div>
  );
};

export default SexoBarChart;
