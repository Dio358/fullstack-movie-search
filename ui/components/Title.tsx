export const Title = ({
    children,
  }: {
    children: React.ReactNode;
  }) => {
  
    return (
      <h1
        style={{
          fontFamily: "'Work Sans', sans-serif",
          color: "white",
          fontSize: "2.5rem",
          fontWeight: 700,
          marginBottom: "1rem",
        }}
      >
        {children}
      </h1>
    );
  };
  