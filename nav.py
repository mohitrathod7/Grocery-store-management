nav_style = '''
.topnav {
    overflow: hidden;
    background-color: #4f3ab7;
    height: 44px;
    font-family: "Baloo Bhai 2", cursive;
}

.topnav a {
    float: left;
    display: block;
    color: #fff;
    text-align: center;
    padding: 12px 6%;
    text-decoration: none;
    font-size: 20px;
    transition: 0.5s all ease-in-out;
    font-family: "Baloo Bhai 2", cursive;
}

.topnav a:hover {
    background-color: #ff0050;
    cursor: pointer;
    color: black;
}

#user{
    float: right
}

#call{
    text-decoration: none;
    color: white;
    padding-left: 3%;
    padding-right: 3%;
}

#a-call, #a-mail, #facebook{
    padding: 12px 2%;
}

#a-mail + svg{
    float: left;
    display: block;
    color: #fff;
    text-align: center;
    padding: 12px 2%;
    text-decoration: none;
    font-size: 20px;
    transition: 0.5s all ease-in-out;
    font-family: "Baloo Bhai 2", cursive;
    transform: translate(-55px, 0px);
}

#a-mail + svg:hover{
    background-color: #ff0050;
    cursor: pointer;
    color: black;
}

@media screen and (max-width: 900px){
    .topnav{
        height: 148px;
    }

    .topnav a{
        font-size: 29.8px;
        padding: 6.2%;
        padding-top: 20px;
        padding-bottom: 20px;
        font-family: "Baloo Bhai 2", cursive;
    }
    
    #facebook, #call, #a-mail{
        padding: 6%;
        padding-left: 12.9%;
        padding-right: 12.9%;
        padding-bottom: 22px;
    }

    #fb-icon, svg{
        transform: translateY(-5px);
    }

    #call{
        transform: translateY(11px);
    }

    #user{
        float: right;
    }

    svg{
        height: 30px;
        width: 30px;
    }
}
'''
