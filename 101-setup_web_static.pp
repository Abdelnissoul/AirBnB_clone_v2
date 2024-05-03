# Define the file structure and symbolic links for web_static
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared/test':
  ensure => 'directory',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

# Create index.html in the test directory
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
                <head>
                </head>
                <body>
                  Holberton School
                </body>
              </html>',
}

# Set permissions for the web_static directory
file { '/data/web_static':
  ensure  => 'directory',
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Configure Apache to serve the static content
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => file('path/to/your/default_configuration_file'),
  notify  => Service['nginx'],
}
