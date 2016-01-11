PACKAGE_VERSION=0.0.1
prefix=/usr

SUBDIRS=src src/objs src/util unittest

clean:
	@for dir in $(SUBDIRS) ; do rm -rf "$$dir/__pycache__" clean ; done

install:
	install -d -m 0755 "$(DESTDIR)/$(prefix)/sbin"
	sed "s/sys.path.append(os.path.join(curDir, \"src\"))/sys.path.append(\"\\/usr\\/lib\\/vworld-server\")/g" vworld-server > "$(DESTDIR)/$(prefix)/sbin/vworld-server"
	chmod 0755 "$(DESTDIR)/$(prefix)/sbin/vworld-server"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/bin"
	install -m 0755 vwctl "$(DESTDIR)/$(prefix)/bin"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/vworld-server"
	cp -r src/* "$(DESTDIR)/$(prefix)/lib/vworld-server"
	find "$(DESTDIR)/$(prefix)/lib/vworld-server" -type f | xargs chmod 644
	find "$(DESTDIR)/$(prefix)/lib/vworld-server" -type d | xargs chmod 755

	install -d -m 0755 "$(DESTDIR)/$(prefix)/share/dbus-1/system-services"
	install -m 0644 data/org.fpemud.VWorld.service "$(DESTDIR)/$(prefix)/share/dbus-1/system-services"

	install -d -m 0755 "$(DESTDIR)/etc/dbus-1/system.d"
	install -m 0644 data/org.fpemud.VWorld.conf "$(DESTDIR)/etc/dbus-1/system.d"

	install -d -m 0755 "$(DESTDIR)/$(prefix)/lib/systemd/system"
	install -m 0644 data/vworld-server.service "$(DESTDIR)/$(prefix)/lib/systemd/system"

uninstall:
	rm -Rf "$(DESTDIR)/$(prefix)/bin/vwctl"
	rm -Rf "$(DESTDIR)/$(prefix)/sbin/vworld-server"
	rm -Rf "$(DESTDIR)/$(prefix)/lib/vworld-server"

.PHONY: all clean install uninstall
