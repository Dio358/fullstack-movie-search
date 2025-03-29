import QuickChart from 'quickchart-js';

export default function createChartUrl(movies: { title: string; rating: string }[]) {
  const chart = new QuickChart();
  chart.setWidth(200);
  chart.setHeight(150);

  chart.setConfig({
    type: 'bar',
    data: {
      labels: movies.map(m => m.title),
      datasets: [
        {
          label: 'Movie Ratings',
          data: movies.map(m => parseFloat(m.rating)),
        },
      ],
    },
  });

  return chart.getUrl();
}
