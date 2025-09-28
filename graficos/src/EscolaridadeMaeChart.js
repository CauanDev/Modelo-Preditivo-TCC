import React, { useRef } from "react";
import Chart from "react-apexcharts";

const EscolaridadeMaeChart = () => {
  const chartRef = useRef(null);

  const categorias = ["Sem estudo", "Fundamental", "Médio", "Superior"];

  const obitos = [42, 48, 8.4, 1.61]; // %
  const sobreviventes = [7.09, 21.27, 47.26, 24.39]; // %

  const options = {
    chart: {
      id: "escolaridade-mae",
      toolbar: { show: false },
    },
    stroke: {
      curve: "smooth",
      width: 3,
    },
    markers: {
      size: 4,
      colors: undefined,
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
      title: { text: "Nível de Escolaridade da Mãe" },
    },
    yaxis: {
      title: { text: "Percentual (%)" },
      min: 0,
      max: 50,
    },
    legend: {
      position: "top",
      horizontalAlign: "center",
    },
    colors: ["#FF4560", "#008FFB"],
    title: {
      text: "Distribuição Percentual da Escolaridade das Mães",
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

export default EscolaridadeMaeChart;
