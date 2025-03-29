import * as React from "react";
import { Movie } from "../interfaces";

type Props = {
  items: Movie[];
  onClick?: (movie: Movie) => void;
  action: string
};

const List: React.FC<Props> = ({ items, onClick , action}) => {
  const [hoveredIndex, setHoveredIndex] = React.useState<number | null>(null);

  return (
    <>
      <span>Click row to {action} favorites</span>
      <ul style={{ listStyleType: "none", padding: 0 }}>
        <div style={{  
          display: "grid", 
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "20px",
        }}>
          <span style={{padding: "5% 0", fontSize: "16px"}}>Title</span>
          <span style={{padding: "5% 0", fontSize: "16px"}}>Release Date</span>
          <span style={{padding: "5% 0", fontSize: "16px"}}>Rating</span>
        </div>
        {items.map((item, index) => (
          <li 
            key={item.id} 
            style={{ 
              marginBottom: "10px",
              backgroundColor: hoveredIndex === index ? 'rgba(109, 152, 199, 0.69)' : 'transparent',
              transition: 'background-color 200ms ease',
              cursor: 'pointer'
            }}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
            onClick={() => onClick && onClick(item)}
          >
            <div style={{  
              display: "grid", 
              gridTemplateColumns: "repeat(3, 1fr)",
              gap: "20px",
            }}>
              <span style={{fontSize: "16px"}}>{item.title}</span>
              <span style={{paddingLeft: "30%", fontSize: "16px"}}>{item.release_date}</span>
              <span style={{paddingLeft: "15%", fontSize: "16px"}}>{item.rating}</span>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default List;