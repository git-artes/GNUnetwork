


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>GNUnetwork/gn/libmac80211/simuladormac.py at master · vagonbar/GNUnetwork · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <link rel="logo" type="image/svg" href="https://github-media-downloads.s3.amazonaws.com/github-logo.svg" />
    <meta property="og:image" content="https://github.global.ssl.fastly.net/images/modules/logos_page/Octocat.png">
    <meta name="hostname" content="github-fe128-cp1-prd.iad.github.net">
    <meta name="ruby" content="ruby 1.9.3p194-tcs-github-tcmalloc (e1c0c3f392) [x86_64-linux]">
    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />
    


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="B31E2C6F:38E0:54E2A:529E6A7A" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="lEIzNrSHBHXPoBvdPuTe8cK99uKscPPzjvgAmcmOlwc=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-fa46bf86884db81851bfd73430b3d71e07fcb3ac.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-62c6a6e51e09f7f4ac5a95b9e7abe014c87b163f.css" media="all" rel="stylesheet" type="text/css" />
    

    

      <script src="https://github.global.ssl.fastly.net/assets/frameworks-5970f5a0a3dcc441d5f7ff74326ffd59bbe9388e.js" type="text/javascript"></script>
      <script src="https://github.global.ssl.fastly.net/assets/github-d90a86ad3d776ad7466f16ce8477627decf55f62.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="0c1382b9ce5023d36bc5adabb0f11f34">

        <link data-pjax-transient rel='permalink' href='/vagonbar/GNUnetwork/blob/0766066a9817b6451641f11dee0e90f51e58af75/gn/libmac80211/simuladormac.py'>
  <meta property="og:title" content="GNUnetwork"/>
  <meta property="og:type" content="githubog:gitrepository"/>
  <meta property="og:url" content="https://github.com/vagonbar/GNUnetwork"/>
  <meta property="og:image" content="https://github.global.ssl.fastly.net/images/gravatars/gravatar-user-420.png"/>
  <meta property="og:site_name" content="GitHub"/>
  <meta property="og:description" content="GNUnetwork - The GNU network project, data networking on GNU Radio"/>

  <meta name="description" content="GNUnetwork - The GNU network project, data networking on GNU Radio" />

  <meta content="4356342" name="octolytics-dimension-user_id" /><meta content="vagonbar" name="octolytics-dimension-user_login" /><meta content="9916365" name="octolytics-dimension-repository_id" /><meta content="vagonbar/GNUnetwork" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="9916365" name="octolytics-dimension-repository_network_root_id" /><meta content="vagonbar/GNUnetwork" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/vagonbar/GNUnetwork/commits/master.atom" rel="alternate" title="Recent Commits to GNUnetwork:master" type="application/atom+xml" />

  </head>


  <body class="logged_out  env-production linux vis-public page-blob">
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join">Sign up</a>
      <a class="button signin" href="/login?return_to=%2Fvagonbar%2FGNUnetwork%2Fblob%2Fmaster%2Fgn%2Flibmac80211%2Fsimuladormac.py">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">

      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
        <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="https://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<input type="text" data-hotkey=" s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    
      data-repo="vagonbar/GNUnetwork"
      data-branch="master"
      data-sha="b23953d102b958b3e85d36dfd5c1f5ef4491d8ce"
  >

    <input type="hidden" name="nwo" value="vagonbar/GNUnetwork" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" title="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
    </div>

  </div>
</div>


      


          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">


  <li>
    <a href="/login?return_to=%2Fvagonbar%2FGNUnetwork"
    class="minibutton with-count js-toggler-target star-button tooltipped upwards"
    title="You must be signed in to use this feature" rel="nofollow">
    <span class="octicon octicon-star"></span>Star
  </a>

    <a class="social-count js-social-count" href="/vagonbar/GNUnetwork/stargazers">
      0
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2Fvagonbar%2FGNUnetwork"
        class="minibutton with-count js-toggler-target fork-button tooltipped upwards"
        title="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-git-branch"></span>Fork
      </a>
      <a href="/vagonbar/GNUnetwork/network" class="social-count">
        0
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author">
            <a href="/vagonbar" class="url fn" itemprop="url" rel="author"><span itemprop="title">vagonbar</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/vagonbar/GNUnetwork" class="js-current-repository js-repo-home-link">GNUnetwork</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    

    <div class="container">

      <div class="repository-with-sidebar repo-container  ">

        <div class="repository-sidebar">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped leftwards" title="Code">
        <a href="/vagonbar/GNUnetwork" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /vagonbar/GNUnetwork">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped leftwards" title="Issues">
          <a href="/vagonbar/GNUnetwork/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="i" data-selected-links="repo_issues /vagonbar/GNUnetwork/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped leftwards" title="Pull Requests"><a href="/vagonbar/GNUnetwork/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /vagonbar/GNUnetwork/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped leftwards" title="Pulse">
        <a href="/vagonbar/GNUnetwork/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /vagonbar/GNUnetwork/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Graphs">
        <a href="/vagonbar/GNUnetwork/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /vagonbar/GNUnetwork/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Network">
        <a href="/vagonbar/GNUnetwork/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /vagonbar/GNUnetwork/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

            <div class="only-with-full-nav">
              

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/vagonbar/GNUnetwork.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/vagonbar/GNUnetwork.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/vagonbar/GNUnetwork" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/vagonbar/GNUnetwork" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="octicon help tooltipped upwards" title="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>



              <a href="/vagonbar/GNUnetwork/archive/master.zip"
                 class="minibutton sidebar-button"
                 title="Download this repository as a zip file"
                 rel="nofollow">
                <span class="octicon octicon-cloud-download"></span>
                Download ZIP
              </a>
            </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:0a48f652d8eaa514a42e6d333eb63a61 -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/vagonbar/GNUnetwork/find/master" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    role="button" aria-label="Switch branches or tags" tabindex="0">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/vagonbar/GNUnetwork/blob/events2/gn/libmac80211/simuladormac.py"
                 data-name="events2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="events2">events2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/vagonbar/GNUnetwork/blob/master/gn/libmac80211/simuladormac.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/vagonbar/GNUnetwork" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">GNUnetwork</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/vagonbar/GNUnetwork/tree/master/gn" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">gn</span></a></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/vagonbar/GNUnetwork/tree/master/gn/libmac80211" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">libmac80211</span></a></span><span class="separator"> / </span><strong class="final-path">simuladormac.py</strong> <span class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="gn/libmac80211/simuladormac.py" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


  <div class="commit commit-loader file-history-tease js-deferred-content" data-url="/vagonbar/GNUnetwork/contributors/master/gn/libmac80211/simuladormac.py">
    Fetching contributors…

    <div class="participation">
      <p class="loader-loading"><img alt="Octocat-spinner-32-eaf2f5" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32-EAF2F5.gif" width="16" /></p>
      <p class="loader-error">Cannot retrieve contributors at this time</p>
    </div>
  </div>

<div id="files" class="bubble">
  <div class="file">
    <div class="meta">
      <div class="info">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
          <span>166 lines (134 sloc)</span>
        <span>6.21 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
              <a class="minibutton disabled tooltipped leftwards" href="#"
                 title="You must be signed in to make or propose changes">Edit</a>
          <a href="/vagonbar/GNUnetwork/raw/master/gn/libmac80211/simuladormac.py" class="button minibutton " id="raw-url">Raw</a>
            <a href="/vagonbar/GNUnetwork/blame/master/gn/libmac80211/simuladormac.py" class="button minibutton ">Blame</a>
          <a href="/vagonbar/GNUnetwork/commits/master/gn/libmac80211/simuladormac.py" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger disabled empty-icon tooltipped leftwards" href="#"
             title="You must be signed in and on a branch to make or propose changes">
          Delete
        </a>
      </div><!-- /.actions -->

    </div>
        <div class="blob-wrapper data type-python js-blob-data">
        <table class="file-code file-diff">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
<span id="L130" rel="#L130">130</span>
<span id="L131" rel="#L131">131</span>
<span id="L132" rel="#L132">132</span>
<span id="L133" rel="#L133">133</span>
<span id="L134" rel="#L134">134</span>
<span id="L135" rel="#L135">135</span>
<span id="L136" rel="#L136">136</span>
<span id="L137" rel="#L137">137</span>
<span id="L138" rel="#L138">138</span>
<span id="L139" rel="#L139">139</span>
<span id="L140" rel="#L140">140</span>
<span id="L141" rel="#L141">141</span>
<span id="L142" rel="#L142">142</span>
<span id="L143" rel="#L143">143</span>
<span id="L144" rel="#L144">144</span>
<span id="L145" rel="#L145">145</span>
<span id="L146" rel="#L146">146</span>
<span id="L147" rel="#L147">147</span>
<span id="L148" rel="#L148">148</span>
<span id="L149" rel="#L149">149</span>
<span id="L150" rel="#L150">150</span>
<span id="L151" rel="#L151">151</span>
<span id="L152" rel="#L152">152</span>
<span id="L153" rel="#L153">153</span>
<span id="L154" rel="#L154">154</span>
<span id="L155" rel="#L155">155</span>
<span id="L156" rel="#L156">156</span>
<span id="L157" rel="#L157">157</span>
<span id="L158" rel="#L158">158</span>
<span id="L159" rel="#L159">159</span>
<span id="L160" rel="#L160">160</span>
<span id="L161" rel="#L161">161</span>
<span id="L162" rel="#L162">162</span>
<span id="L163" rel="#L163">163</span>
<span id="L164" rel="#L164">164</span>
<span id="L165" rel="#L165">165</span>

            </td>
            <td class="blob-line-code">
                    <div class="highlight"><pre><div class='line' id='LC1'><span class="c"># -*- coding: utf-8 -*-</span></div><div class='line' id='LC2'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC3'><span class="sd">Created on Tue May 28 14:55:46 2013</span></div><div class='line' id='LC4'><br/></div><div class='line' id='LC5'><span class="sd">@author: belza, ggomez</span></div><div class='line' id='LC6'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC7'><br/></div><div class='line' id='LC8'><span class="kn">import</span> <span class="nn">sys</span></div><div class='line' id='LC9'><span class="n">sys</span><span class="o">.</span><span class="n">path</span> <span class="o">+=</span><span class="p">[</span><span class="s">&#39;..&#39;</span><span class="p">]</span></div><div class='line' id='LC10'><br/></div><div class='line' id='LC11'><span class="kn">import</span> <span class="nn">Queue</span></div><div class='line' id='LC12'><span class="kn">import</span> <span class="nn">libmanagement.NetworkConfiguration</span> <span class="kn">as</span> <span class="nn">NetworkConfiguration</span></div><div class='line' id='LC13'><span class="kn">import</span> <span class="nn">libmanagement.DiscoveryPeeringController</span> <span class="kn">as</span> <span class="nn">DiscoveryPeeringController</span></div><div class='line' id='LC14'><span class="kn">import</span> <span class="nn">libmanagement.Beacon</span> <span class="kn">as</span> <span class="nn">Beacon</span></div><div class='line' id='LC15'><span class="kn">import</span> <span class="nn">libadaptationlayer.schedEvToFr</span> <span class="kn">as</span> <span class="nn">schedEvToFr</span></div><div class='line' id='LC16'><span class="kn">import</span> <span class="nn">libadaptationlayer.schedFrToEv</span> <span class="kn">as</span> <span class="nn">schedFrToEv</span></div><div class='line' id='LC17'><span class="kn">import</span> <span class="nn">ieee80211mac</span> <span class="kn">as</span> <span class="nn">Mac</span></div><div class='line' id='LC18'><span class="kn">import</span> <span class="nn">libvirtualchannel.virtualchannel</span> <span class="kn">as</span> <span class="nn">virtualchannel</span></div><div class='line' id='LC19'><br/></div><div class='line' id='LC20'><span class="k">def</span> <span class="nf">simulates</span><span class="p">():</span></div><div class='line' id='LC21'><br/></div><div class='line' id='LC22'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;-------------------NODE 1: MAC Addr 100-------------------------------------------------------&quot;</span>    </div><div class='line' id='LC23'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Layer 3 packet queues&quot;</span></div><div class='line' id='LC24'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_rx_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC25'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_tx_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC26'><br/></div><div class='line' id='LC27'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Configuration of the Scheduler of Node 1 that recieves frames and generates management events.&quot;</span></div><div class='line' id='LC28'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_rx_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC29'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ctrl_q1</span><span class="p">,</span> <span class="n">mgmt_q1</span><span class="p">,</span> <span class="n">data_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC30'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues1</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC31'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Ctrl&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">ctrl_q1</span><span class="p">),</span> \</div><div class='line' id='LC32'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Mgmt&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">mgmt_q1</span><span class="p">),</span> \</div><div class='line' id='LC33'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Data&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">data_q1</span><span class="p">)</span>  \</div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch1</span> <span class="o">=</span> <span class="n">schedFrToEv</span><span class="o">.</span><span class="n">SchedFrToEv</span><span class="p">(</span><span class="n">frame_rx_q1</span><span class="p">,</span> <span class="n">out_queues1</span><span class="p">)</span></div><div class='line' id='LC36'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch1</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC37'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC38'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Configuration of the scheduler of Node 1 that recieves events and generates frame events.&quot;</span></div><div class='line' id='LC39'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_tx_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC40'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx_ev_q1</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC41'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues_tx1</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC42'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;frames&#39;</span><span class="p">:</span>    <span class="p">(</span><span class="n">frame_tx_q1</span><span class="p">)</span> \</div><div class='line' id='LC43'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC44'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx1</span> <span class="o">=</span> <span class="n">schedEvToFr</span><span class="o">.</span><span class="n">SchedEvToFr</span><span class="p">(</span><span class="n">tx_ev_q1</span><span class="p">,</span> <span class="n">out_queues_tx1</span><span class="p">)</span></div><div class='line' id='LC45'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx1</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC46'><br/></div><div class='line' id='LC47'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Network configuration: the MAC Addr, the name of the network and the broadcast Addr&quot;</span>    </div><div class='line' id='LC48'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf1</span> <span class="o">=</span> <span class="n">NetworkConfiguration</span><span class="o">.</span><span class="n">NetworkConfiguration</span><span class="p">(</span><span class="s">&quot;100&quot;</span><span class="p">,</span><span class="s">&#39;my network&#39;</span><span class="p">,</span><span class="s">&quot;256&quot;</span><span class="p">,</span><span class="mi">1</span><span class="p">)</span></div><div class='line' id='LC49'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf1</span><span class="o">.</span><span class="n">retry_timeout</span> <span class="o">=</span> <span class="mi">5</span>    </div><div class='line' id='LC50'><br/></div><div class='line' id='LC51'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Starts the Controller of The FSM for Peering Discovering&quot;</span></div><div class='line' id='LC52'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol1</span> <span class="o">=</span>  <span class="n">DiscoveryPeeringController</span><span class="o">.</span><span class="n">DiscoveryPeeringController</span><span class="p">(</span><span class="n">net_conf1</span><span class="p">,</span><span class="bp">None</span><span class="p">,</span><span class="n">mgmt_q1</span><span class="p">,</span><span class="n">tx_ev_q1</span><span class="p">)</span></div><div class='line' id='LC53'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">## dpcontrol1 =  DiscoveryPeeringController.DiscoveryPeeringController(net_conf1,None,pkt_tx_q1,pkt_rx_q1)</span></div><div class='line' id='LC54'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol1</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC55'><br/></div><div class='line' id='LC56'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Start the MAC controller&quot;</span></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl1</span> <span class="o">=</span> <span class="n">Mac</span><span class="o">.</span><span class="n">ControllerMAC</span><span class="p">(</span> <span class="n">net_conf1</span><span class="p">,</span> <span class="n">ctrl_q1</span><span class="p">,</span> <span class="n">mgmt_q1</span><span class="p">,</span> <span class="n">data_q1</span><span class="p">,</span> <span class="n">tx_ev_q1</span><span class="p">,</span> <span class="n">pkt_rx_q1</span><span class="p">,</span> <span class="n">pkt_tx_q1</span> <span class="p">)</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl1</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC59'><br/></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Starts the beacon generator of this node&quot;</span></div><div class='line' id='LC61'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon1</span> <span class="o">=</span> <span class="n">Beacon</span><span class="o">.</span><span class="n">Beacon</span><span class="p">(</span><span class="n">net_conf1</span> <span class="p">,</span><span class="n">tx_ev_q1</span><span class="p">)</span></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon1</span><span class="o">.</span><span class="n">start</span><span class="p">()</span>    </div><div class='line' id='LC63'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;---------------------END NODE 1 -----------------------------------------------&quot;</span></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC65'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;-------------------NODE 2: MAC Addr 101-------------------------------------------------------&quot;</span>    </div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Layer 3 packet queues&quot;</span></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_rx_q2</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC68'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_tx_q2</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC69'><br/></div><div class='line' id='LC70'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Configuration of the Scheduler of Node 2 that recieves frames and generates management events.&quot;</span></div><div class='line' id='LC71'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_rx_q2</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ctrl_q2</span><span class="p">,</span> <span class="n">mgmt_q2</span><span class="p">,</span> <span class="n">data_q2</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues2</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Ctrl&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">ctrl_q2</span><span class="p">),</span> \</div><div class='line' id='LC75'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Mgmt&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">mgmt_q2</span><span class="p">),</span> \</div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Data&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">data_q2</span><span class="p">)</span>  \</div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC78'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch2</span> <span class="o">=</span> <span class="n">schedFrToEv</span><span class="o">.</span><span class="n">SchedFrToEv</span><span class="p">(</span><span class="n">frame_rx_q2</span><span class="p">,</span> <span class="n">out_queues2</span><span class="p">)</span></div><div class='line' id='LC79'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch2</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Configuration of the scheduler of Node 2 that recieves events and generates frame events.&quot;</span></div><div class='line' id='LC82'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; The frames tx queue is the same for all nodes ( = frame_tx_q1) to simulates a shared medium&quot;</span></div><div class='line' id='LC83'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_tx_q2</span> <span class="o">=</span> <span class="n">frame_tx_q1</span></div><div class='line' id='LC84'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx_ev_q2</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC85'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues_tx2</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;frames&#39;</span><span class="p">:</span>    <span class="p">(</span><span class="n">frame_tx_q2</span><span class="p">)</span> \</div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx2</span> <span class="o">=</span> <span class="n">schedEvToFr</span><span class="o">.</span><span class="n">SchedEvToFr</span><span class="p">(</span><span class="n">tx_ev_q2</span><span class="p">,</span> <span class="n">out_queues_tx2</span><span class="p">)</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx2</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC90'><br/></div><div class='line' id='LC91'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Network configuration: the MAC Addr, the name of the network and the broadcast Addr&quot;</span>    </div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf2</span> <span class="o">=</span> <span class="n">NetworkConfiguration</span><span class="o">.</span><span class="n">NetworkConfiguration</span><span class="p">(</span><span class="s">&quot;101&quot;</span><span class="p">,</span><span class="s">&#39;my network&#39;</span><span class="p">,</span><span class="s">&quot;256&quot;</span><span class="p">,</span><span class="mi">1</span><span class="p">)</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf2</span><span class="o">.</span><span class="n">retry_timeout</span> <span class="o">=</span> <span class="mi">5</span>    </div><div class='line' id='LC94'><br/></div><div class='line' id='LC95'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Starts the Controller of The FSM for Peering Discovering&quot;</span></div><div class='line' id='LC96'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol2</span> <span class="o">=</span>  <span class="n">DiscoveryPeeringController</span><span class="o">.</span><span class="n">DiscoveryPeeringController</span><span class="p">(</span><span class="n">net_conf2</span><span class="p">,</span><span class="bp">None</span><span class="p">,</span><span class="n">mgmt_q2</span><span class="p">,</span><span class="n">tx_ev_q2</span><span class="p">)</span></div><div class='line' id='LC97'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol2</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC98'><br/></div><div class='line' id='LC99'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Start the MAC controller&quot;</span></div><div class='line' id='LC100'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl2</span> <span class="o">=</span> <span class="n">Mac</span><span class="o">.</span><span class="n">ControllerMAC</span><span class="p">(</span> <span class="n">net_conf2</span><span class="p">,</span> <span class="n">ctrl_q2</span><span class="p">,</span> <span class="n">mgmt_q2</span><span class="p">,</span> <span class="n">data_q2</span><span class="p">,</span> <span class="n">tx_ev_q2</span><span class="p">,</span> <span class="n">pkt_rx_q2</span><span class="p">,</span> <span class="n">pkt_tx_q2</span> <span class="p">)</span></div><div class='line' id='LC101'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl2</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC102'><br/></div><div class='line' id='LC103'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Starts the beacon generator of this node&quot;</span></div><div class='line' id='LC104'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon2</span> <span class="o">=</span> <span class="n">Beacon</span><span class="o">.</span><span class="n">Beacon</span><span class="p">(</span><span class="n">net_conf2</span> <span class="p">,</span><span class="n">tx_ev_q2</span><span class="p">)</span></div><div class='line' id='LC105'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon2</span><span class="o">.</span><span class="n">start</span><span class="p">()</span>  </div><div class='line' id='LC106'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC107'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;-------------------END NODE 101-------------------------------------------------------&quot;</span>    </div><div class='line' id='LC108'>&nbsp;&nbsp;</div><div class='line' id='LC109'><br/></div><div class='line' id='LC110'>&nbsp;</div><div class='line' id='LC111'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;-------------------NODE 3: MAC Addr 102-------------------------------------------------------&quot;</span>    </div><div class='line' id='LC112'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Layer 3 packet queues&quot;</span></div><div class='line' id='LC113'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_rx_q3</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC114'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pkt_tx_q3</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC115'><br/></div><div class='line' id='LC116'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Configuration of the Scheduler of Node 3 that recieves frames and generates management events.&quot;</span></div><div class='line' id='LC117'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_rx_q3</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC118'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ctrl_q3</span><span class="p">,</span> <span class="n">mgmt_q3</span><span class="p">,</span> <span class="n">data_q3</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">),</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC119'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues3</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC120'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Ctrl&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">ctrl_q3</span><span class="p">),</span> \</div><div class='line' id='LC121'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Mgmt&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">mgmt_q3</span><span class="p">),</span> \</div><div class='line' id='LC122'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Data&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">data_q3</span><span class="p">)</span>  \</div><div class='line' id='LC123'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC124'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch3</span> <span class="o">=</span> <span class="n">schedFrToEv</span><span class="o">.</span><span class="n">SchedFrToEv</span><span class="p">(</span><span class="n">frame_rx_q3</span><span class="p">,</span> <span class="n">out_queues3</span><span class="p">)</span></div><div class='line' id='LC125'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sch3</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC126'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC127'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Configuration of the scheduler of Node 3 that recieves events and generates frame events.&quot;</span></div><div class='line' id='LC128'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; The frames tx queue is the same for all nodes ( = frame_tx_q1) to simulates a shared medium&quot;</span></div><div class='line' id='LC129'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">frame_tx_q3</span> <span class="o">=</span> <span class="n">frame_tx_q1</span></div><div class='line' id='LC130'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx_ev_q3</span> <span class="o">=</span> <span class="n">Queue</span><span class="o">.</span><span class="n">Queue</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span></div><div class='line' id='LC131'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">out_queues_tx3</span> <span class="o">=</span> <span class="p">{</span> \</div><div class='line' id='LC132'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;frames&#39;</span><span class="p">:</span>    <span class="p">(</span><span class="n">frame_tx_q3</span><span class="p">)</span> \</div><div class='line' id='LC133'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC134'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx3</span> <span class="o">=</span> <span class="n">schedEvToFr</span><span class="o">.</span><span class="n">SchedEvToFr</span><span class="p">(</span><span class="n">tx_ev_q3</span><span class="p">,</span> <span class="n">out_queues_tx3</span><span class="p">)</span></div><div class='line' id='LC135'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">tx3</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC136'><br/></div><div class='line' id='LC137'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Network configuration: the MAC Addr, the name of the network and the broadcast Addr&quot;</span>    </div><div class='line' id='LC138'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf3</span> <span class="o">=</span> <span class="n">NetworkConfiguration</span><span class="o">.</span><span class="n">NetworkConfiguration</span><span class="p">(</span><span class="s">&quot;102&quot;</span><span class="p">,</span><span class="s">&#39;my network&#39;</span><span class="p">,</span><span class="s">&quot;256&quot;</span><span class="p">,</span><span class="mi">1</span><span class="p">)</span></div><div class='line' id='LC139'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">net_conf3</span><span class="o">.</span><span class="n">retry_timeout</span> <span class="o">=</span> <span class="mi">5</span>    </div><div class='line' id='LC140'><br/></div><div class='line' id='LC141'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Starts the Controller of The FSM for Peering Discovering&quot;</span></div><div class='line' id='LC142'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol3</span> <span class="o">=</span>  <span class="n">DiscoveryPeeringController</span><span class="o">.</span><span class="n">DiscoveryPeeringController</span><span class="p">(</span><span class="n">net_conf3</span><span class="p">,</span><span class="bp">None</span><span class="p">,</span><span class="n">mgmt_q3</span><span class="p">,</span><span class="n">tx_ev_q3</span><span class="p">)</span></div><div class='line' id='LC143'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">dpcontrol3</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC144'><br/></div><div class='line' id='LC145'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; Start the MAC controller&quot;</span></div><div class='line' id='LC146'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl3</span> <span class="o">=</span> <span class="n">Mac</span><span class="o">.</span><span class="n">ControllerMAC</span><span class="p">(</span> <span class="n">net_conf3</span><span class="p">,</span> <span class="n">ctrl_q3</span><span class="p">,</span> <span class="n">mgmt_q3</span><span class="p">,</span> <span class="n">data_q3</span><span class="p">,</span> <span class="n">tx_ev_q3</span><span class="p">,</span> <span class="n">pkt_rx_q3</span><span class="p">,</span> <span class="n">pkt_tx_q3</span> <span class="p">)</span></div><div class='line' id='LC147'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">macctrl3</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC148'><br/></div><div class='line' id='LC149'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;Starts the beacon generator of this node&quot;</span></div><div class='line' id='LC150'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon3</span> <span class="o">=</span> <span class="n">Beacon</span><span class="o">.</span><span class="n">Beacon</span><span class="p">(</span><span class="n">net_conf3</span> <span class="p">,</span><span class="n">tx_ev_q3</span><span class="p">)</span></div><div class='line' id='LC151'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">myBeacon3</span><span class="o">.</span><span class="n">start</span><span class="p">()</span>  </div><div class='line' id='LC152'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot;---------------------END NODO 102 -----------------------------------------------&quot;</span></div><div class='line' id='LC153'><br/></div><div class='line' id='LC154'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vc</span><span class="o">=</span> <span class="n">virtualchannel</span><span class="o">.</span><span class="n">VirtualChannel</span><span class="p">(</span><span class="n">frame_tx_q2</span><span class="p">)</span></div><div class='line' id='LC155'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vc</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">frame_rx_q1</span><span class="p">)</span> </div><div class='line' id='LC156'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vc</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">frame_rx_q2</span><span class="p">)</span></div><div class='line' id='LC157'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vc</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">frame_rx_q3</span><span class="p">)</span></div><div class='line' id='LC158'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">vc</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></div><div class='line' id='LC159'><br/></div><div class='line' id='LC160'><br/></div><div class='line' id='LC161'><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&#39;__main__&#39;</span><span class="p">:</span></div><div class='line' id='LC162'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC163'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">simulates</span><span class="p">()</span></div><div class='line' id='LC164'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">except</span> <span class="ne">KeyboardInterrupt</span><span class="p">:</span></div><div class='line' id='LC165'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">pass</span></div></pre></div>
            </td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2013 <span title="0.06491s from github-fe128-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/vagonbar/GNUnetwork/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" title="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      title="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

