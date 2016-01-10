PACKAGE_VERSION=0.0.1
prefix=/usr

SUBDIRS=src src/objs src/util unittest

clean:
	@for dir in $(SUBDIRS) ; do rm -rf "$$dir/__pycache__" clean ; done

install:
	install -d -m 0755 "$(DESTDIR)/$(prefix)/sbin"
	sed "s/sys.path.append(\".\\/src\")/sys.path.append(\"\\/usr\\/lib\\/vworld-server\")/g" vworld-server > "$(DESTDIR)/$(prefix)/sbin/vworld-server"
	chmod 0755 "$(DESTDIR)/$(prefix)/sbin/vworld-server"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/bin"
	install -m 0755 vwctl "$(DESTDIR)/$(prefix)/bin"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/vworld-server"
	cp -r src/* "$(DESTDIR)/$(prefix)/lib/vworld-server"
	find "$(DESTDIR)/$(prefix)/lib/vworld-server" -type f | xargs chmod 644
	find "$(DESTDIR)/$(prefix)/lib/vworld-server" -type d | xargs chmod 755

uninstall:
	rm -Rf "$(DESTDIR)/$(prefix)/bin/vwctl"
	rm -Rf "$(DESTDIR)/$(prefix)/sbin/vworld-server"
	rm -Rf "$(DESTDIR)/$(prefix)/lib/vworld-server"

.PHONY: all clean install uninstall
