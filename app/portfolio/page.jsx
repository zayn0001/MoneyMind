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
import { Button } from "@/components/ui/button"
import PortfolioTable from "../components/PortfolioTable"
import { Input } from "@/components/ui/input"
import Info from "../components/Info"

export default function Portfolio() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [data, setData] = useState(null);
  const [company, setCompany] = useState("")
  const [loading, setLoading] = useState(true);
  const [portfolio, setPortfolio] = useState([])
  const [advices, setAdvices] = useState([{name:"microsoft", sentiment:1.57}, {name:"apple", sentiment:0.123}])

  const handleaddcompany = async () => {
    try {
      const response = await fetch("/backend/addcompany", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${user.accessToken}`,
          'Content-Type': 'application/json'
        },
        body:JSON.stringify({company:company})
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const responseData = await response.json();
      console.log(responseData)
      //setPortfolio(previous=>{[...previous, {"name":company}]})
      fetchportfolio(user.accessToken)
      setCompany("")
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  const fetchportfolio = async (accessToken) => {
    try {
      const response = await fetch("/backend/getcompany", {
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
      setPortfolio(responseData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fetchadvices = async (accessToken) => {
    try {
      const response = await fetch("/backend/getportfolio", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
  
      const responseData = await response.json();
      console.log(responseData, "908098098")
      setAdvices(responseData.message);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect( () => {
    const auth = getAuth();

    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        console.log(currentUser)
        setUser(currentUser);
        fetchportfolio(currentUser.accessToken)
        fetchadvices(currentUser.accessToken)
        setLoading(false)
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
      <div className='flex flex-row m-auto'>
        <div style={{width:"50%", height:"80vh", margin:"auto"}}>
          <div style={{justifyContent:"center", display:"flex", alignItems:"center", alignContent:"center", height:"50%", width:"100%", flexDirection:"column"}}>
          <PortfolioTable invoices={portfolio} fetchportfolio={fetchportfolio} user={user}></PortfolioTable>
          </div>
          <div style={{justifyContent:"center", display:"flex", alignItems:"center",alignContent:"center", height:"50%", width:"100%", flexDirection:"column"}}>
            <Input className='w-[50%]' type="text" placeholder="microsoft" value={company} onChange={(e)=>setCompany(e.target.value)} />
            <Button 
            variant="outline" 
            onClick={handleaddcompany} 
            style={{ backgroundColor: "white", color: "black", marginTop:20 }}
            >
            Add
          </Button>
          </div>
        </div>
      <div className='border border-white rounded m-10' style={{justifyContent:"flex-start", display:"flex", alignItems:"end", height:"80vh", width:"50%", flexDirection:"column"} }>
        {advices.map((comp)=>(
          <Info key={comp.name} company={comp.name} sentiment={comp.advice}></Info>
        ))}
      </div>
      </div>
    </>
  )
  
}
