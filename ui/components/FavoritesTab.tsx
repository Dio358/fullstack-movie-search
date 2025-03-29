import List from "./List";

export const FavoritesTab = (props: {
    items: ({ id: number; title: string; rating: string; release_date: string })[],
    src: string
}) => {

    

    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "13%"
    }}>
        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Favorites</h1>
        <List items={props.items} action="remove from"/>

        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Average Score</h1>
        <img src={props.src} alt="Chart of average scores"/>
    </div>;
}