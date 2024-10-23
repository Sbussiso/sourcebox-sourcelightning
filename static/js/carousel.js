document.addEventListener('DOMContentLoaded', function () {
    var myCarousel = document.querySelector('#carouselExampleCaptions');
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval: false,
        wrap: true
    });

    document.getElementById('carousel-button').addEventListener('click', function() {
        const messageDiv = document.getElementById('carousel-message');
        const activeItem = document.querySelector('.carousel-item.active');

        if (activeItem.id === 'carousel-item-1') {
            messageDiv.innerHTML = `
                <div class="container">
                  <br/>
                  <br/>
                  <h1 class="white-text">Apps</h1>
                  <br/>
                  <div class="row">
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">File Reader</h5>
                              <p class="card-text">An app for reading and querying various file formats on your local Machine.</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#fileReaderModal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">PC Scanner</h5>
                              <p class="card-text">An AI tool for analyzing your system load and specs to provide a system state summary</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app2Modal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">Wallpaper Generator</h5>
                              <p class="card-text">Easily Generate and set wallpapers for your PC</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app3Modal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">Vanilla GPT</h5>
                              <p class="card-text">Quickly access and use ChatGPT in your local console</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app4Modal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">Vanilla Mistral</h5>
                              <p class="card-text">Quickly access and use Mistral in your local console</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app5Modal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">Vanilla Gemini</h5>
                              <p class="card-text">Quickly access and use Gemini in your local console</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app6Modal">Download</a>
                            </div>
                          </div>
                      </div>
                      <div class="col-md-4">
                          <div class="card custom-card">
                            <div class="card-body">
                              <h5 class="card-title">Vanilla Claud</h5>
                              <p class="card-text">Quickly access and use Claud in your local console</p>
                              <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#app7Modal">Download</a>
                            </div>
                          </div>
                      </div>
                  </div>
                </div>
            `;
        }

        if (activeItem.id === 'carousel-item-2') {
            messageDiv.innerHTML = `
                <br/>
                <br/> 
                <h1 class="white-text">Agents</h1>
                <p>We recommend using Local Command Agent in a virtual machine for security. More updates will be needed.</p>
                <br/>
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="card custom-card">
                              <div class="card-body">
                                <h5 class="card-title">Google Agent</h5>
                                <p class="card-text">Run an agent connected to your google accounts</p>
                                <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#agent1Modal">Download</a>
                              </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card custom-card">
                              <div class="card-body">
                                <h5 class="card-title">Code Agent</h5>
                                <p class="card-text">An agent with a code interpreter and stack exchange knowledge</p>
                                <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#agent2Modal">Download</a>
                              </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card custom-card">
                              <div class="card-body">
                                <h5 class="card-title">Local Command Agent</h5>
                                <p class="card-text">An agent with access to your command line and a file toolkit</p>
                                <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#agent3Modal">Download</a>
                              </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card custom-card">
                              <div class="card-body">
                                <h5 class="card-title">Finance Agent</h5>
                                <p class="card-text">An agent equipped with tools to give you the latest stock news and info</p>
                                <a href="#" class="card-link" data-bs-toggle="modal" data-bs-target="#agent4Modal">Download</a>
                              </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        if (activeItem.id === 'carousel-item-3') {
            messageDiv.innerHTML = `
                <br/>
                <br/> 
                <h1 class="white-text">Lightning Builder</h1>
                <p>Design and experiment with custom lightning effects for your projects.</p>
                <br/>
                <div class="container">
                    <!-- Lightning Builder content -->
                </div>
            `;
        }
    });

    // Change button text and link based on active carousel item
    myCarousel.addEventListener('slid.bs.carousel', function () {
        const activeItem = document.querySelector('.carousel-item.active');
        const button = document.getElementById('carousel-button');

        if (activeItem.id === 'carousel-item-3') {
            button.textContent = 'Open Lightning Builder';
            button.onclick = function() {
                window.location.href = '/build-landing';
            };
        } else {
            button.textContent = 'Show Downloads';
            button.onclick = function() {
                // Default action for other items
            };
        }
    });
});
