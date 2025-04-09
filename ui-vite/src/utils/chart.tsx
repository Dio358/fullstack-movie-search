import QuickChart from "quickchart-js";
import { Movie } from "../interfaces";
import { BarChart } from "@mui/x-charts/BarChart";

export default function createChartUrl(movies: Movie[]) {
  const chart = new QuickChart();
  chart.setWidth(200);
  chart.setHeight(150);

  chart.setConfig({
    type: "bar",
    data: {
      labels: movies.map((m) => m.title),
      datasets: [
        {
          label: "Movie Ratings",
          data: movies.map((m) => parseFloat(m.vote_average)),
        },
      ],
    },
  });

  return chart.getUrl();
}

export const createBarChart = (movies: Movie[] | null) => {
  if (!movies) return null;
  const chart = (
    <BarChart
      xAxis={[
        {
          scaleType: "band",
          data: movies.map((m) => m.title),
          label: "Movies",
          tickLabelStyle: { fill: "whitesmoke" },
          labelStyle: { fill: "whitesmoke" },
        },
      ]}
      yAxis={[
        {
          label: "Rating",
          tickLabelStyle: { fill: "whitesmoke" },
          labelStyle: { fill: "whitesmoke" },
        },
      ]}
      series={[
        {
          data: movies.map((m) => parseFloat(m.vote_average)),
          label: "Movie Ratings",
          color: "whitesmoke",
        },
      ]}
      width={400}
      height={300}
      slotProps={{
        legend: {
          labelStyle: {
            fill: "whitesmoke",
          },
        },
      }}
    />
  );

  return chart;
};
