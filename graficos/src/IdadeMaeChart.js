import React, { useRef } from "react";
import Chart from "react-apexcharts";

const IdadeDaMarChart = () => {
  const chartRef = useRef(null);

  const categorias = ["< 20 anos", "20-29 anos", "30-39 anos", "40+ anos"];

  const obitos = [30, 40, 5, 25]; // %
  const sobreviventes = [5, 30, 50, 15]; // %

  const options = {
    chart: {
      id: "idade-mae",
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
      title: { text: "Faixa etária da mãe" },
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
    colors: ["#FF4560", "#008FFB"],
    title: {
      text: "Distribuição da Idade das Mães",
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

export default IdadeDaMarChart;
