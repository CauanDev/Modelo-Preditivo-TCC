import React, { useRef } from "react";
import Chart from "react-apexcharts";

const MortesCidadeChart = () => {
  const chartRef = useRef(null);

  const cidades = [
    "Campo Grande",
    "Dourados",
    "Três Lagoas",
    "Corumbá",
    "Ponta Porã",
  ];

  const obitos = [25, 20, 15, 20, 20]; // %
  const sobreviventes = [35, 25, 15, 15, 10]; // %

  const options = {
    chart: {
      id: "mortes-cidades",
      toolbar: { show: false },
    },
    stroke: {
      curve: "smooth",
      width: 3,
    },
    markers: {
      size: 4,
      strokeWidth: 3,
    },
    dataLabels: {
      offsetY: -10,
      enabled: true,
      formatter: (val) => `${val}%`,
      style: {
        fontWeight: "bold",
      },
      background: {
        enabled: true,
        foreColor: "#fff",
        color: "#000",
        borderRadius: 2,
        opacity: 0.9,
      },
    },
    xaxis: {
      categories: cidades,
      title: { text: "Cidade" },
    },
    yaxis: {
      title: { text: "Percentual (%)" },
      min: 0,
      max: 100,
    },
    legend: {
      position: "top",
      horizontalAlign: "center",
    },
    colors: ["#FF4560", "#008FFB"], // vermelho para óbitos, azul para sobreviventes
    title: {
      text: "Percentual de Mortes nas 5 maiores cidades do Mato Grosso do Sul",
      align: "center",
    },
  };

  const series = [
    { name: "Óbitos ≤ 1 ano", data: obitos },
    { name: "Sobreviventes > 1 ano", data: sobreviventes },
  ];

  return (
    <div>
      <Chart
        ref={chartRef}
        options={options}
        series={series}
        type="line"
        height={400}
      />
    </div>
  );
};

export default MortesCidadeChart;
