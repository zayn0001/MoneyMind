"use client"
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { app, auth } from '../config';
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react";
import CircularProgress from '@mui/material/CircularProgress';
import SignOutButton from "../components/SignOutButton";
import LargeText from "../components/LargeText"
import SmallText from "../components/SmallText"
import NavBar from "../components/NavBar"
import Info from '../components/Info';

export default function Portfolio() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sentiments, setSentiments] = useState([{name:"microsoft", sentiment:1.57}, {name:"apple", sentiment:0.123}])

  const fetchBackendData = async (accessToken) => {
    try {
      const response = await fetch("/backend/python", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
  
      const responseData = await response.json();
      console.log(responseData)
      setData(responseData.message);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    const auth = getAuth();

    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        console.log(currentUser)
        setUser(currentUser);
        fetchBackendData(currentUser.accessToken);
      } else {
        router.push('/signin'); 
      }
    });

    return () => unsubscribe();
  }, []);

  if (!user || loading) {
    return (<>
    <div style={{justifyContent:"center", display:"flex", alignItems:"center", alignContent:"center", height:"100vh", flexDirection:"column"}}>
    <CircularProgress color="secondary" size={"3em"} />
    </div>
    </>
    ); 
  }

    return (
      
    <>
      <NavBar user={user}/>
      <div className='border border-white rounded m-auto mt-10' style={{justifyContent:"flex-start", display:"flex", alignItems:"end", height:"80vh", width:"90%", flexDirection:"column"} }>
        {sentiments.map((comp)=>(
          <Info key={comp.name} company={comp.name} sentiment={comp.sentiment}></Info>
        ))}
      </div>
    </>
  )
  
}
