import * as React from "react";
import { Movie } from "../interfaces";
import { useEffect } from "react";
import styles from './scrollableList.module.css';

type Props = {
  items: Movie[];
  length?: number
  onClick?: (movie: Movie) => void;
  onHover?: (index: Movie | null) => void | null;
  action: string;
};

const List: React.FC<Props> = ({ items, length = Number.POSITIVE_INFINITY, onClick, onHover = null, action }) => {
  const [hoveredIndex, setHoveredIndex] = React.useState<number | null>(null);
  
  useEffect(() => {
    if (onHover) {
      onHover(items?.at(hoveredIndex) || null);
    }
  }, [hoveredIndex, onHover, items]);
  
  return (
    <>
      <span>Click row to {action} favorites</span>
      <div style={{
        width: "95%",
        borderRadius: "5px",
        overflow: "hidden",
      }}>
        {/* Header */}
        <div style={{
          backgroundColor: "rgba(17, 124, 231, 0.63)",
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          padding: "16px",
          borderTopLeftRadius: "5px",
          borderTopRightRadius: "5px",
        }}>
          <span style={{ fontSize: "16px" }}>Title</span>
          <span style={{ fontSize: "16px" }}>Release Date</span>
          <span style={{ fontSize: "16px" }}>Rating</span>
        </div>
        
        {/* Content */}
        <div 
          className={styles.scrollable}
          style={{
            background: "white",
            borderBottomLeftRadius: "5px",
            borderBottomRightRadius: "5px",
            maxHeight: "300px", 
            overflowY: "auto",
          }}
        >
          <ul style={{ 
            listStyleType: "none", 
            padding: 0, 
            margin: 0 
          }}>
            {items && items.map((item, index) => (
              index < length && (
              <li
                key={item.id}
                style={{
                  backgroundColor: hoveredIndex === index ? "rgba(109, 152, 199, 0.69)" : "transparent",
                  transition: "background-color 200ms ease",
                  cursor: "pointer",
                  padding: "10px 16px", 
                }}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
                onClick={() => onClick?.(item)}
              >
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(3, 1fr)",
                  }}
                >
                  <span style={{ fontSize: "16px" }}>{item.title}</span>
                  <span style={{ fontSize: "16px" }}>{item.release_date}</span>
                  <span style={{ fontSize: "16px" }}>{item.vote_average}</span>
                </div>
              </li>)
            ))}
          </ul>
        </div>
      </div>
    </>
  );
};

export default List;