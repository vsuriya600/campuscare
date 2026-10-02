const BASE_URL = "http://127.0.0.1:8000"


// ======================================
// REGISTER
// ======================================

async function registerUser(){

    const message =
    document.getElementById("register_message")

    message.innerText = ""

    const data = {

        full_name:
        document.getElementById("full_name").value,

        institutional_id:
        document.getElementById("institutional_id").value,

        password:
        document.getElementById("password").value,

        role:
        document.getElementById("role").value
    }

    try{

        const response = await fetch(
            `${BASE_URL}/register`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)
            }
        )

        const result = await response.json()

        if(response.ok){

            message.innerText =
            "Register Success"

            message.className =
            "text-success text-center mt-3 fw-bold"

            setTimeout(()=>{

                window.location.href =
                "login.html"

            },2000)

        }else{

            message.innerText =
            result.detail || "Registration Failed"

            message.className =
            "text-danger text-center mt-3 fw-bold"
        }

    }catch(error){

        message.innerText =
        "Server Error"

        message.className =
        "text-danger text-center mt-3 fw-bold"

        console.log(error)
    }
}



// ======================================
// LOGIN
// ======================================

async function loginUser(){

    const message =
    document.getElementById("login_message")

    message.innerText = ""

    const data = {

        institutional_id:
        document.getElementById("institutional_id").value,

        password:
        document.getElementById("password").value
    }

    try{

        const response = await fetch(
            `${BASE_URL}/login`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)
            }
        )

        const result = await response.json()

        if(response.ok){

            localStorage.setItem(
                "token",
                result.access_token
            )

            localStorage.setItem(
                "role",
                result.role
            )

            localStorage.setItem(
                "user_id",
                result.user_id
            )

            localStorage.setItem(
                "full_name",
                result.full_name
            )

            message.innerText =
            "Login Successful"

            message.className =
            "text-success text-center mt-3 fw-bold"

            setTimeout(()=>{

                window.location.href =
                "dashboard.html"

            },2000)

        }else{

            message.innerText =
            result.detail || "Login Failed"

            message.className =
            "text-danger text-center mt-3 fw-bold"
        }

    }catch(error){

        message.innerText =
        "Server Error"

        message.className =
        "text-danger text-center mt-3 fw-bold"

        console.log(error)
    }
}



// ======================================
// SUBMIT COMPLAINT
// ======================================

async function submitComplaint(){

    const userId =
    localStorage.getItem("user_id")

    const data = {

        user_id:userId,

        title:
        document.getElementById("title").value,

        description:
        document.getElementById("description").value,

        zone:
        document.getElementById("zone").value,

        building_name:
        document.getElementById("building_name").value,

        room_or_area:
        document.getElementById("room_or_area").value
    }

    try{

        const response = await fetch(
            `${BASE_URL}/complaints`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)
            }
        )

        const result = await response.json()

        console.log(result)

        loadComplaints()

        loadDashboardStats()

        document.getElementById("title").value = ""
        document.getElementById("description").value = ""
        document.getElementById("building_name").value = ""
        document.getElementById("room_or_area").value = ""

    }catch(error){

        console.log(error)
    }
}



// ======================================
// LOAD USER COMPLAINTS
// ======================================

async function loadComplaints(){

    const userId =
    localStorage.getItem("user_id")

    try{

        const response = await fetch(
            `${BASE_URL}/complaints/user/${userId}`
        )

        const complaints = await response.json()

        const container =
        document.getElementById("complaints_container")

        if(!container) return

        container.innerHTML = ""

        complaints.forEach((complaint)=>{

            let badgeClass = "pending"

            if(complaint.status === "resolved"){
                badgeClass = "resolved"
            }

            if(complaint.status === "assigned"){
                badgeClass = "assigned"
            }

            container.innerHTML += `

            <div class="complaint-card">

                <h5>
                    ${complaint.title}
                </h5>

                <p>
                    ${complaint.description}
                </p>

                <p>
                    <strong>Location:</strong>

                    ${complaint.building_name},
                    ${complaint.room_or_area}
                </p>

                <span class="status-badge ${badgeClass}">
                    ${complaint.status}
                </span>

            </div>
            `
        })

    }catch(error){

        console.log(error)
    }
}



// ======================================
// DASHBOARD STATS
// ======================================

async function loadDashboardStats(){

    try{

        const response = await fetch(
            `${BASE_URL}/dashboard/stats`
        )

        const stats = await response.json()

        document.getElementById("total_count")
        .innerText = stats.total

        document.getElementById("pending_count")
        .innerText = stats.pending

        document.getElementById("resolved_count")
        .innerText = stats.resolved

    }catch(error){

        console.log(error)
    }
}


// ======================================
// DASHBOARD COMPLAINT LISTS
// ======================================

async function loadDashboardComplaints(){

    try{

        const response = await fetch(`${BASE_URL}/complaints`)
        const complaints = await response.json()
        const pendingContainer = document.getElementById("dashboard_pending_complaints")
        const resolvedContainer = document.getElementById("dashboard_resolved_complaints")

        if(!pendingContainer || !resolvedContainer) return

        const pending = complaints.filter(complaint => complaint.status !== "resolved")
        const resolved = complaints.filter(complaint => complaint.status === "resolved")

        const renderComplaint = complaint => `
            <div class="complaint-card">
                <h5>${complaint.title}</h5>
                <p>${complaint.description}</p>
                <p><strong>Status:</strong> ${complaint.status}</p>
                <p><strong>Location:</strong> ${complaint.building_name}, ${complaint.room_or_area}</p>
            </div>
        `

        pendingContainer.innerHTML = pending.length
            ? pending.map(renderComplaint).join("")
            : "<p>No pending complaints.</p>"

        resolvedContainer.innerHTML = resolved.length
            ? resolved.map(renderComplaint).join("")
            : "<p>No solved complaints.</p>"

    }catch(error){

        console.log(error)
    }
}



// ======================================
// LOAD ADMIN COMPLAINTS
// ======================================

async function loadAdminComplaints(){

    try{

        const response = await fetch(
            `${BASE_URL}/complaints`
        )

        const complaints = await response.json()

        const container =
        document.getElementById("admin_complaints")

        if(!container) return

        container.innerHTML = ""

        complaints.forEach((complaint)=>{

            container.innerHTML += `

            <div class="complaint-card">

                <h5>
                    ${complaint.title}
                </h5>

                <p>
                    ${complaint.description}
                </p>

                <p>
                    <strong>Status:</strong>

                    ${complaint.status}
                </p>

                <p>
                    <strong>Location:</strong>

                    ${complaint.building_name},
                    ${complaint.room_or_area}
                </p>

                ${
                    complaint.status === "resolved"

                    ?

                    `
                    <button
                        class="btn btn-success btn-sm"
                        disabled
                    >
                        Marked
                    </button>
                    `

                    :

                    `
                    <button
                        class="btn btn-danger btn-sm"
                        onclick="updateComplaintStatus(${complaint.complaint_id}, 'resolved')"
                    >
                        Mark Resolved
                    </button>
                    `
                }

            </div>
            `
        })

    }catch(error){

        console.log(error)
    }
}



// ======================================
// UPDATE COMPLAINT STATUS
// ======================================

async function updateComplaintStatus(id, status){

    try{

        await fetch(
            `${BASE_URL}/complaints/${id}`,
            {
                method:"PATCH",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    status:status
                })
            }
        )

        loadAdminComplaints()

        loadDashboardStats()

        loadDashboardComplaints()

        loadComplaints()

    }catch(error){

        console.log(error)
    }
}



// ======================================
// ROLE BASED UI
// ======================================

function setupRoleBasedUI(){

    const role =
    localStorage.getItem("role")

    const adminMenu =
    document.getElementById("admin_menu")

    if(role === "admin"){

        if(adminMenu){

            adminMenu.style.display =
            "block"
        }

        loadAdminComplaints()
    }
}



// ======================================
// PROFILE INFO
// ======================================

function loadProfile(){

    const fullName =
    localStorage.getItem("full_name")

    const role =
    localStorage.getItem("role")

    const profileName =
    document.getElementById("profile_name")

    const profileRole =
    document.getElementById("profile_role")

    const welcomeName =
    document.getElementById("welcome_name")

    if(profileName){

        profileName.innerText =
        fullName
    }

    if(profileRole){

        profileRole.innerText =
        role
    }

    if(welcomeName){

        welcomeName.innerText =
        fullName
    }
}



// ======================================
// LOGOUT
// ======================================

function logout(){

    localStorage.clear()

    window.location.href =
    "login.html"
}



// ======================================
// AUTO LOAD
// ======================================

if(window.location.pathname.includes("dashboard.html")){

    loadComplaints()

    loadDashboardStats()

    loadDashboardComplaints()

    setupRoleBasedUI()

    loadProfile()
}
