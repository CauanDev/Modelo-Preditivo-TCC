import React, { useRef } from "react";
import Chart from "react-apexcharts";

const RacaCorChart = () => {
  const chartRef = useRef(null);

  const categorias = ["Branca", "Parda", "Preta", "Indígena", "Amarela"];

  const obitos = [20, 45, 25, 8, 2]; // %
  const sobreviventes = [40, 35, 15, 5, 5]; // %

  const options = {
    chart: {
      id: "raca-cor",
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
      categories: categorias,
      title: { text: "Raça/Cor" },
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
      text: "Distribuição por Raça/Cor",
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

export default RacaCorChart;
