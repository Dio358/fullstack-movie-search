import QuickChart from 'quickchart-js';
import { Movie } from '../interfaces';

export default function createChartUrl(movies: Movie[]) {
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
          data: movies.map(m => parseFloat(m.vote_average)),
        },
      ],
    },
  });

  return chart.getUrl();
}
