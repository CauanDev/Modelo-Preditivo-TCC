import React from "react";
import CidadeChart from "./CidadeChart";
import EscolaridadeMaeChart from "./EscolaridadeMaeChart";
import IdadeMaeChart from "./IdadeMaeChart";
import OcupacaoChartMae from "./OcupacaoChartMae";
import RacaCorChart from "./RacaCorChart";
import SexoBarChart from "./SexoBarChart";

const App = () => {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ textAlign: "center", marginBottom: "40px" }}>Dashboard de Indicadores</h1>

      <h2>Cidades</h2>
      <CidadeChart />

      <h2>Escolaridade das Mães</h2>
      <EscolaridadeMaeChart />

      <h2>Idade das Mães</h2>
      <IdadeMaeChart />

      <h2>Ocupação das Mães</h2>
      <OcupacaoChartMae />

      <h2>Raça/Cor</h2>
      <RacaCorChart />

      <h2>Sexo</h2>
      <SexoBarChart />
    </div>
  );
};

export default App;
