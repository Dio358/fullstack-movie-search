export const SideBar = (props: { onClick: () => void, state: number, onClick1: () => void, onClick2: () => void,  onClick3: () => void }) => {
    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        alignContent: "flex-end"
    }}>
        <button
            onClick={props.onClick}
            style={{
                marginTop: "15px",
                padding: "10px 20px",
                backgroundColor: props.state !== 1 ? "rgba(17, 124, 231, 0.35)" : "rgba(17, 124, 231, 0.63)",
                color: "white",
                border: "solid",
                borderRadius: "5px",
                fontFamily: "Arial",
                cursor: "pointer"
            }}
        >
            Discover
        </button>
        <button
            onClick={props.onClick1}
            style={{
                marginTop: "15px",
                padding: "10px 20px",
                backgroundColor: props.state !== 2 ? "rgba(17, 124, 231, 0.35)" : "rgba(17, 124, 231, 0.63)",
                color: "white",
                border: "solid",
                borderRadius: "5px",
                fontFamily: "Arial",
                cursor: "pointer"
            }}
        >
            Favorites
        </button>
        <button
            onClick={props.onClick2}
            style={{
                marginTop: "15px",
                padding: "10px 20px",
                backgroundColor: props.state !== 2 ? "rgba(17, 124, 231, 0.35)" : "rgba(17, 124, 231, 0.63)",
                color: "white",
                border: "solid",
                borderRadius: "5px",
                fontFamily: "Arial",
                cursor: "pointer"
            }}
        >
            Search Movie
        </button>
        <button
            onClick={props.onClick3}
            style={{
                marginTop: "15px",
                padding: "10px 20px",
                backgroundColor: "rgba(17, 124, 231, 0.35)",
                color: "white",
                border: "solid",
                borderRadius: "5px",
                fontFamily: "Arial",
                cursor: "pointer"
            }}
        >
            Log Out
        </button>
    </div>;
}