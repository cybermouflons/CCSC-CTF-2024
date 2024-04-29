<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="">
        <meta name="author" content="">
        <title>Andromeda Image Gallery</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Open+Sans&display=swap" rel="stylesheet">
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/bootstrap-icons.css" rel="stylesheet">
        <link href="css/templatemo-topic-listing.css" rel="stylesheet">      
    </head>
    
    <body id="top">

        <main>

            <nav class="navbar navbar-expand-lg">
                <div class="container">
                    <a class="navbar-brand" href="/">
                        <i class="bi-back"></i>
                        <span>Underground Watch</span>
                    </a>

                    <div class="d-lg-none ms-auto me-4">
                        <a href="#top" class="navbar-icon bi-person smoothscroll"></a>
                    </div>
    
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
    
                </div>
            </nav>
            

            <section class="hero-section d-flex justify-content-center align-items-center" id="section_1">
                <div class="container">
                    <div class="row">

                        <div class="col-lg-8 col-12 mx-auto">
                            <h1 class="text-white text-center">Upload Image</h1>

                            <h6 class="text-center">and let the resistance continue its work...</h6>

                            <form method="post" action="/upload.php" enctype="multipart/form-data" class="custom-form mt-4 pt-2 mb-lg-0 mb-5">
                                <div class="input-group input-group-lg">

                                    <input name="file" type="file" class="form-control border-0 mt-3" id="keyword" placeholder="Choose image...">
                                    <button type="submit" class="form-control">Upload</button>

                                </div>
                            </form>
                        </div>

                    </div>
                </div>
            </section>

            <section class="explore-section section-padding" id="section_2">
                <div class="container">

                        <div class="col-12 text-center">
                            <h2 class="mb-4">Browse Images</h1>
                        </div>

                    </div>
                </div>

                <div class="container">
                    <div class="row">

                        <div class="col-12">
                            <div class="tab-content" id="myTabContent">
                                <div class="tab-pane fade show active" id="design-tab-pane" role="tabpanel" aria-labelledby="design-tab" tabindex="0">
                                    <div class="row">
                                        <div class="col-lg-4 col-md-6 col-12 mb-4 mb-lg-0">
                                            <div class="custom-block bg-white shadow-lg">
                                                <a href="/">
                                                    <div class="d-flex">
                                                        <div>
                                                            <h5 class="mb-2">The Data Breach</h5>
                                                            <p class="mb-0">A lone hacker from The Andromeda Initiative infiltrates OrionTech's secure servers, surrounded by cascading lines of code. In the background, the OrionTech logo looms as digital security barriers crumble under the hacker's expertise.</p>
                                                        </div>

                                                        <span class="badge bg-design rounded-pill ms-auto">14</span>
                                                    </div>

                                                    <img src="images/image1.png" class="custom-block-image img-fluid" alt="">
                                                </a>
                                            </div>
                                        </div>

                                        <div class="col-lg-4 col-md-6 col-12 mb-4 mb-lg-0">
                                            <div class="custom-block bg-white shadow-lg">
                                                <a href="/">
                                                    <div class="d-flex">
                                                        <div>
                                                            <h5 class="mb-2">Surveillance Drones</h5>
                                                            <p class="mb-0">Stealthy surveillance drones hover amidst the neon-lit streets of Cyprus, blending into the urban landscape as they silently monitor OrionTech's movements with glowing red eyes and advanced scanning capabilities.</p>
                                                        </div>

                                                        <span class="badge bg-design rounded-pill ms-auto">75</span>
                                                    </div>

                                                    <img src="images/image2.png" class="custom-block-image img-fluid" alt="">
                                                </a>
                                            </div>
                                        </div>

                                        <div class="col-lg-4 col-md-6 col-12">
                                            <div class="custom-block bg-white shadow-lg">
                                                <a href="/">
                                                    <div class="d-flex">
                                                        <div>
                                                            <h5 class="mb-2">Virtual Reconnaissance</h5>
                                                            <p class="mb-0">Inside a virtual realm resembling a labyrinthine network, members of The Andromeda Initiative gather around a holographic display, engaged in virtual reconnaissance. They navigate encrypted data streams and bypass digital security measures to uncover the truth hidden within the digital realm.</p>
                                                        </div>

                                                        <span class="badge bg-design rounded-pill ms-auto">100</span>
                                                    </div>

                                                    <img src="images/image3.png" class="custom-block-image img-fluid" alt="">
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>                              
                            </div>
                    </div>
                </div>
            </section>
         
        </main>

        <!-- JAVASCRIPT FILES -->
        <script src="js/jquery.min.js"></script>
        <script src="js/bootstrap.bundle.min.js"></script>
        <script src="js/jquery.sticky.js"></script>
        <script src="js/click-scroll.js"></script>
        <script src="js/custom.js"></script>

    </body>
</html>
